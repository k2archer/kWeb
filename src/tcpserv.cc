
/* Copyright 2016<Copyright Pwei> */

#include "k_socket.h"
#include "k_unit_test.h"
#include "k_web.h"
#include <pthread.h>

const int kBacklog = 128;

#define MAXN 16384
#define MAXLINE 4096


typedef void (*sigal_funcation)(int);

sigal_funcation Signal(int signo, sigal_funcation func)
{
  struct sigaction act;
  
  act.sa_handler = func;
  sigemptyset(&act.sa_mask);

  if (signo == SIGALRM) {
#ifdef  SA_INTERRUPT
    act.sa_flags |= SA_INTERRUPT;
#endif
  } else {
#ifdef  SA_RESTART
    act.sa_flags |= SA_RESTART;
#endif    
  }

  struct sigaction oact;
  if (sigaction(signo, &act, &oact) < 0)
    return SIG_ERR;

  return oact.sa_handler;
}

void SigalChild(int signo)
{
  int status;
  pid_t pid;
  while ( (pid = waitpid(-1, &status, WNOHANG)) > 0)
    ;
    // printf("child %d terminated\n", pid);

  return;
}

void WebChild(int sockfd)
{
   FILE* fpin;
   char request[BUFSIZE];

   fpin = fdopen(sockfd, "r");
   if (fpin == NULL) {
      fprintf(stderr, "WebChild \e[1;32m fplin:%d sockfd:%d %s\e[0m\n",
                 fpin, sockfd, strerror(errno));
      return;
   }
   fgets(request, BUFSIZE, fpin);
   // printf("got a call: request = %s\n", request);
   read_til_crnl(fpin);

   process_rq(request, sockfd);
   fclose(fpin);
}

typedef struct {
  pthread_t thread_tid;
  long thread_count;
} Thread;

Thread* g_tptr;
int g_listenfd;
int nthreads = 2;
socklen_t g_addrlen;
pthread_mutex_t g_mlock = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t g_clock = PTHREAD_MUTEX_INITIALIZER;

void ThreadInt(int signo)
{
  printf("\n");
  for (int i = 0; i < nthreads; i++) {
     printf("i:%d ptid:%d count:%d\n", i, g_tptr[i].thread_tid, g_tptr[i].thread_count);
  }
  exit(0);
}

void* ThreadMain(void* argc)
{
  long i = (long)argc;
  int connfd;

  socklen_t clilen;
  struct sockaddr* cliaddr;
  cliaddr = (struct sockaddr*)malloc(g_addrlen);

  printf("thread %d starting\n", i);

  for (;;) {
    clilen = g_addrlen;
    
    pthread_mutex_lock(&g_mlock);
    connfd = Accept(g_listenfd, cliaddr, &clilen);
    // connfd = Accept(g_listenfd, NULL, NULL);
    pthread_mutex_unlock(&g_mlock);

    g_tptr[i].thread_count++;

    WebChild(connfd);
    // close(connfd);
  }
}

void ThreadMake(int i)
{
  pthread_create(&g_tptr[i].thread_tid, NULL, &ThreadMain, (void*) i);
  return;
}

int main(int argc, char const *argv[])
{
  g_listenfd = TcpListen(kServerPort, kBacklog);
  // g_listenfd = Tcp_listen(NULL, "9999", &g_addrlen);

  Signal(SIGCHLD, SigalChild);
  signal(SIGINT, ThreadInt);

  g_tptr = (Thread*)calloc(nthreads, sizeof(Thread));
  
  for (int i = 0; i < nthreads; i++)
    ThreadMake(i);

  for (;;)
    pause();

  printf("return\n");
  return 0;
}
