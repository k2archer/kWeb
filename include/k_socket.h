
/* Copyright 2016<Copyright Pwei> */

#ifndef K_SOCKET_H_
#define K_SOCKET_H_

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <poll.h>
// #include <sys/epoll.h>
#include <limits.h>
#include <sys/resource.h>
#include <sys/param.h>

typedef struct sockaddr SA;

extern const int kMaxLine    = 4096;
extern const int kServerPort = 80;

void err_quit(const char* str)
{
	char buff[kMaxLine];
	
	switch (errno)
	{
		case (ECONNREFUSED) :
			sprintf(buff, "ECONNREFUSED"); break;
		case (ETIMEDOUT) :
			sprintf(buff, "ETIMEDOUT");    break;
		case (EHOSTUNREACH) :
			sprintf(buff, "EHOSTUNREACH"); break;
		case (ENETUNREACH) :
			sprintf(buff, "ENETUNREACH");  break;
		
		case (EADDRINUSE) :
			sprintf(buff, "EADDRINUSE");  break;

		default: break;
	}

	fprintf(stderr, "\e[1;32m  %s: %s : %s \e[0m \n", str, buff, strerror(errno));

	exit(1);
}

int Socket(int family, int type, int protocol)
{
	int n;
	if ( (n = socket(family, type, protocol)) < 0)
		err_quit("socket error");
	return n;
}

void Setsockopt(int fd, int level, int optname, const void *optval, socklen_t optlen)
{
	if (setsockopt(fd, level, optname, optval, optlen) < 0)
		err_quit("setsockopt error");
}

int Bind(int sockfd, SA * addr, socklen_t addrlen)
{
	int n;
	if ( (n = bind(sockfd, addr, addrlen)) < 0)
		err_quit("bind error");
	return n;
}

void Listen(int sockfd, int backlog)
{
	char* ptr;
	if ( (ptr = getenv("LISTENQ")) != NULL)
		backlog = atoi(ptr);

	if (listen(sockfd, backlog) < 0)
		err_quit("listen error");
}

int Accept(int sockfd, SA* cliaddr, socklen_t *addrlen)
{
	int n;
	if ( (n = accept(sockfd, cliaddr, addrlen)) < 0)
		err_quit("accept error");
	return n;
}

int TcpListen(int port, int backlog)
{
  int listenfd = Socket(AF_INET, SOCK_STREAM, 0);

  struct sockaddr_in servaddr;
  bzero(&servaddr, sizeof(servaddr));
  servaddr.sin_family = AF_INET;
  servaddr.sin_port   = htons(port);
  servaddr.sin_addr.s_addr = htonl(INADDR_ANY);

  const int on = 1;
  Setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));

  Bind(listenfd, (SA *) &servaddr, sizeof(servaddr));

  Listen(listenfd, backlog);

  return listenfd;
}

int Select(int maxfdpl, fd_set* readset, fd_set* writeset, 
				fd_set* exceptset, struct timeval* timeout)
{
	int n;
	if ( (n = select(maxfdpl, readset, writeset, exceptset, timeout)) < 0)
		err_quit("select error");

	return n;
}

int Fork()
{
	int n;
	if ( (n = fork()) < 0)
		err_quit("fork error");
	return n;
}

int Connect(int sockfd, SA * servaddr, socklen_t addrlen)
{
	int n;
	if ( (n = connect(sockfd, servaddr, addrlen)) < 0)
		err_quit("connect error");
	return n;
}

int Inet_pton(int family, const char *strptr, void *addrptr)
{
    if (family == AF_INET) {
    	struct in_addr  in_val;

        if (inet_aton(strptr, &in_val)) {
            memcpy(addrptr, &in_val, sizeof(struct in_addr));
            return (1);
        }
		return(0);
    }
	errno = EAFNOSUPPORT;
    return (-1);
}

char * Fgets(char *ptr, int n, FILE *stream)
{
	char	*rptr;

	if ( (rptr = fgets(ptr, n, stream)) == NULL && ferror(stream)) {
		printf("fputs error");
		exit(1);
	}

	return (rptr);
}

ssize_t Readline(int sockfd, void* vptr, size_t maxlen)
{
	ssize_t n , rc;
	char c;
	char* ptr = (char*)vptr;

	for (n = 1; n < maxlen; n++) {
	again:
		if ( (rc = read(sockfd, &c, 1)) == 1) {
			*ptr++ = c;
			if (c == '\n')
				break;
		} else if (rc == 0 ) {
			*ptr = 0;
			return n -1;
		} else {
			if (errno == EINTR)
				goto again;
			return -1;
		}
	}
	*ptr = 0;
	printf("n:%d\n", n);
	return n;
}










#include <netdb.h>
#define LISTENQ     1024
int
tcp_listen(const char *host, const char *serv, socklen_t *addrlenp)
{
	int				listenfd, n;
	const int		on = 1;
	struct addrinfo	hints, *res, *ressave;

	bzero(&hints, sizeof(struct addrinfo));
	hints.ai_flags = AI_PASSIVE;
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;

	if ( (n = getaddrinfo(host, serv, &hints, &res)) != 0)
		// err_quit("tcp_listen error for %s, %s: %s",
		// 		 host, serv, gai_strerror(n));
		err_quit("getaddrinfo error");
	ressave = res;

	do {
		listenfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
		if (listenfd < 0)
			continue;		/* error, try next one */

		Setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));
		if (bind(listenfd, res->ai_addr, res->ai_addrlen) == 0)
			break;			/* success */

		close(listenfd);	/* bind error, close and try next one */
	} while ( (res = res->ai_next) != NULL);

	if (res == NULL)	/* errno from final socket() or bind() */
		// err_sys("tcp_listen error for %s, %s", host, serv);
		err_quit("tcp_listen error");

	Listen(listenfd, LISTENQ);

	if (addrlenp)
		*addrlenp = res->ai_addrlen;	/* return size of protocol address */

	freeaddrinfo(ressave);

	return(listenfd);
}
/* end tcp_listen */

/*
 * We place the wrapper function here, not in wraplib.c, because some
 * XTI programs need to include wraplib.c, and it also defines
 * a Tcp_listen() function.
 */

int
Tcp_listen(const char *host, const char *serv, socklen_t *addrlenp)
{
	return(tcp_listen(host, serv, addrlenp));
}

#endif  // K_SOCKET_H_ 
