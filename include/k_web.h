
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUFSIZE 4096
#define SERVER_STRING "Server: k_httpd/0.1.0\r\n"

void cannot_do(int fd)
{
	printf("cannot_do\n");
	FILE* fp = fdopen(fd, "w");
	fprintf(fp, "HTTP/1.0 501 Not Implemented\r\n");
	fprintf(fp, "Content - type: text/plain\r\n");
	fprintf(fp, "\r\n");
	fprintf(fp, "That command is not yet implemented\r\n");
	fclose(fp);
}

void cat(int client, FILE *resource)
{
	printf("cat\n");
 char buf[1024];

 fgets(buf, sizeof(buf), resource);
 while (!feof(resource))
 {
  send(client, buf, strlen(buf), 0);
  printf("sned: %s\n", buf);
  fgets(buf, sizeof(buf), resource);
 }
}

void headers(int client, const char *filename)
{
	printf("headers\n");
 char buf[1024];
 (void)filename;  /* could use filename to determine file type */

 strcpy(buf, "HTTP/1.0 200 OK\r\n");
 send(client, buf, strlen(buf), 0);
 strcpy(buf, SERVER_STRING);
 send(client, buf, strlen(buf), 0);
 sprintf(buf, "Content-Type: text/html\r\n");
 send(client, buf, strlen(buf), 0);
 strcpy(buf, "\r\n");
 send(client, buf, strlen(buf), 0);
}

int get_line(int sock, char *buf, int size)
{
 int i = 0;
 char c = '\0';
 int n;

 while ((i < size - 1) && (c != '\n'))
 {
  n = recv(sock, &c, 1, 0);
  /* DEBUG printf("%02X\n", c); */
  if (n > 0)
  {
   if (c == '\r')
   {
    n = recv(sock, &c, 1, MSG_PEEK);
    /* DEBUG printf("%02X\n", c); */
    if ((n > 0) && (c == '\n'))
     recv(sock, &c, 1, 0);
    else
     c = '\n';
   }
   buf[i] = c;
   i++;
  }
  else
   c = '\n';
 }
 buf[i] = '\0';
 
 return(i);
}

void serve_file(int client, const char *filename)
{
	printf("filename:%s\n", filename);
 FILE *resource = NULL;
 // int numchars = 1;
 // char buf[1024];

 // buf[0] = 'A'; buf[1] = '\0';
 // while ((numchars > 0) && strcmp("\n", buf))  /* read & discard headers */
 //  numchars = get_line(client, buf, sizeof(buf));

 resource = fopen(filename, "r");
 if (resource == NULL)
  cannot_do(client);
 else
 {
  // headers(client, filename);
  cat(client, resource);
 }
 fclose(resource);
}

void read_til_crnl(FILE* fp)
{
	char buff[BUFSIZE];
	while( fgets(buff, BUFSIZE, fp) != NULL && strcmp(buff, "\r\n") != 0)
		;
}

void header(FILE* fp, char* content_type)
{
	fprintf(fp, "HTTP/1.0 200 OK\r\n");
	fprintf(fp, "%s", SERVER_STRING);
	if (content_type )
		fprintf(fp, "Content - type: %s\r\n", content_type);
	// fprintf(fp, "\r\n");
}


void do_404(char* item, int fd)
{
	printf("do_404()\n");
	FILE* fp = fdopen(fd, "w");
	fprintf(fp, "HTTP/1.0 404 Not Found\r\n");
	fprintf(fp, "Content - type: text/plain\r\n");
	fprintf(fp, "\t\n");

	fprintf(fp, "The item you requested: %s\r\nis not found\r\n", item);
	fclose(fp);
}

int isadir(char* f)
{
	struct stat info;
	return ( stat(f, &info) != -1 && S_ISDIR(info.st_mode) );
}

int not_exist(char* f)
{
	struct stat info;
	int ret = stat(f, &info);
	return ( ret == -1);
}

void do_ls(char* dir, int fd)
{
	printf("do_ls\n");

	char path[1024];
	strcpy(path, dir);
	strcat(path, "index.html" );
	printf("%s\n", path);
	struct stat st;
	if (stat(path, &st) != -1) {
		serve_file(fd, path);
		close(fd);
		return;
	} 

	headers(fd, NULL);

	FILE* fp;
	fp = fdopen(fd, "w");
	// header(fp, "text\plain");
	// fprintf(fp, "\r\n");
	fflush(fp);

	dup2(fd, 1);
	dup2(fd, 2);
	close(fd);

	execlp("ls", "ls", "-1", dir, NULL);
	perror(dir);	
}

char* file_type(char* f)
{
	char* cp;
	if ( (cp = strrchr(f, '.')) != NULL)
		return cp + 1;

	return "";
}

int ends_in_cgi(char* f)
{
	return ( strcmp(file_type(f), "cgi") == 0);
}

void do_exec(char* prog, int fd, char* argc)
{
	printf("do_exec\n");

	headers(fd, NULL);

	// FILE* fp;
	// fp = fdopen(fd, "w");
	// header(fp, NULL);
	// fflush(fp);
	dup2(fd, 1);
	dup2(fd, 2);
	close(fd);
	char * argv[ ]={"","","",(char *)0};
	argv[1] = prog;
	argv[2] = argc;
	char * env[ ]={"PATH=/bin",0};
	execve("/bin/bash",argv,env);
	close(fd);
	exit(11);

}

void do_cat(char* f, int fd)
{
	printf("do_cat\n");
	char* extension = file_type(f);
	char* content = "text/plain";
	FILE* fpsock;
	FILE* fpfile;
	int c;

	if ( strcmp(extension, "html") == 0)
		content = "text/html";
	else if (strcmp(extension, "gif") == 0)
		content = "image/git";
	else if (strcmp(extension, "jpg") == 0 )
		content = "image/jpeg";
	else if (strcmp(extension, "jpeg") == 0)
		content = "image/jpeg";
	else if (strcmp(extension, "js") == 0)
		content = "application/javascript";
	else if (strcmp(extension, "css") == 0)
		content = "text/css";

	// serve_file(fd, f);
	// close(fd);
	// return;

	fpsock = fdopen(fd, "w");
	fpfile = fopen(f, "r");
	if (fpsock != NULL && fpfile != NULL)
	{
		header(fpsock, content);
		fprintf(fpsock, "\r\n");
		while( (c = getc(fpfile)) != EOF)
			putc(c, fpsock);
		fclose(fpfile);
		fclose(fpsock);
	} else {
		printf("fopen error\n");
	}
}

void process_rq(char* rq, int fd)
{
	printf("process_rq fd:%d\n", fd);
	char cmd[BUFSIZE], arg[BUFSIZE];
	char protocol_version[128];
	int pid;
//	if ( (pid = fork()) != 0)
//		return;
	if ((pid = fork()) < 0) {
		return;
	} else if ( pid == 0) {
		strcpy(arg, "./");
		if ( sscanf(rq, "%s %s %s", cmd, arg+2, protocol_version) != 3)
			exit(19);

		printf("CMD:%s path:%s protocol:%s\n", cmd, arg, protocol_version);

		char path[BUFSIZE];
		char argcs[BUFSIZE];
		if ( sscanf(arg, "%[^?]?%s", path, argcs) < 1)
			exit(19);
		printf("path:%s argcs:%s\n", path, argcs);

		int ret = strcmp(cmd, "GET");
		if ( ret != 0)
			cannot_do(fd);
		else if ( not_exist(path) )
			do_404(path, fd);
		else if ( isadir(path) )
			do_ls(path, fd);
		else if ( ends_in_cgi(path) )
			do_exec(path, fd, argcs);
		else
			do_cat(path, fd);

		printf("OK");
		// close(fd);
		int status;
//		waitpid(pid, &status, 0);
		exit(11);
	} else {
		if (waitpid(pid, NULL, 0) != pid) {                        /* 父进程必须为一代子进程收尸 */
			printf("fork 1st child_proc success. 1st child_proc killed...\n");
		}
		return;
	}



}

