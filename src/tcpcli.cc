
/* Copyright 2016<Copyright Pwei> */

#include "k_socket.h"
#include "k_unit_test.h"

const int kMaxTesting = 30;

void Client(FILE* fp, int sockfd)
{
  char sendline[kMaxLine], recvline[kMaxLine];
  while (Fgets(sendline, kMaxLine, fp) != NULL) {
    printf("fgets(%d): %s\n", strlen(sendline), sendline);

    write(sockfd, sendline, strlen(sendline));

    if (Readline(sockfd, recvline, kMaxLine) == 0) {
      printf("str_cli: server terminated prematurely\n");
    }

    printf("pid:%d fd:%d received(%d): %s\n", getpid(), sockfd, strlen(recvline), recvline);
  }
  close(sockfd);
}

void ClientChild(int sockfd)
{
  char sendline[kMaxLine];
  char received[kMaxLine];
  for(int i=0; i < kMaxTesting; i++) {
    sprintf(sendline, "pid:%d fd:%d :%d\n", getpid(), sockfd, i);
    write(sockfd, sendline, strlen(sendline));
    int n;
    if ((n = read(sockfd, received, kMaxLine)) > 0) {
      EXPECT_EQ_STR(sendline, received);
    }

    // sleep(1);
  }

  printf("pid(%d):fd(%d) %d/%d (%3.2f%%) passed\n", \
          getpid(), sockfd, test_pass, test_count, test_pass * 100.0 / test_count);

  close(sockfd);
}

int main(int argc, char const *argv[])
{
  if (argc < 2) {
    printf("usage: tcpcli <IPaddress>\n");
    printf("usage: tcpcli <IPaddress> [ConnectNumber]\n");
    exit(1);
  }

  int max_connects  = 5;
  if (argc == 3)
    max_connects = atoi(argv[2]);

  int i, sockfd[max_connects];
  struct sockaddr_in server_addr;

  for (i = 0; i < max_connects; i++)
  { 
    sockfd[i] = Socket(AF_INET, SOCK_STREAM, 0);

    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port   = htons(kServerPort);
    Inet_pton(AF_INET, argv[1], &server_addr.sin_addr);

    Connect(sockfd[i], (SA *) &server_addr, sizeof(server_addr));

    if ( i > 0)
    switch (Fork()) {
      case 0:
        ClientChild(sockfd[i]);
        _exit(EXIT_SUCCESS);
        break;
      case -1:
        printf("Can't create child (%s)\n", strerror(errno));
      close(sockfd[i]);
      break;
      default: break;
    }

  }

  Client(stdin, sockfd[0]);

  return 0;
}
