
/* Copyright 2016<Copyright Pwei> */

#ifndef K_UNIT_TEST_H_
#define K_UNIT_TEST_H_

static int main_ret   = 0;
static int test_count = 0;
static int test_pass  = 0;

#define EXPECT_EQ_BASE(equality, expect, actual, format) \
    do {\
        test_count++; \
        if (equality) \
            test_pass++; \
        else { \
            fprintf(stderr, "%s:%d: expect: " format " actual: " format "\n", __FILE__, __LINE__, expect, actual); \
            main_ret = 1; \
        } \
    } while(0)

#define EXPECT_EQ_INT(expect, actual) \
    EXPECT_EQ_BASE( (expect) == (actual), expect, actual, "%d")

#define EXPECT_EQ_STR(expect, actual) \
    EXPECT_EQ_BASE( !strcmp(expect, actual), expect, actual, "%s")

#include <sys/resource.h>

#ifndef HAVE_GETRUSAGE_PROTO
    int getrusage(int, struct rusage*);
#endif

void pr_cpu_time()
{
    printf("pr_cpu_time\n");
    double user, sys;
    struct rusage myusage, childusage;

    if ( getrusage(RUSAGE_SELF, &myusage) < 0 ) {
        printf("getrusage error\n");
        exit(1);
    }
    if ( getrusage(RUSAGE_CHILDREN, &childusage) < 0) {
        printf("getrusage error\n");
        exit(1);        
    }

    user = (double) myusage.ru_utime.tv_sec +
                    myusage.ru_utime.tv_usec / 1000000.0;
    user += (double) childusage.ru_utime.tv_sec +
                    childusage.ru_utime.tv_usec / 1000000.0;

    sys = (double) myusage.ru_stime.tv_sec +
                    myusage.ru_stime.tv_usec / 1000000.0;
    sys += (double) childusage.ru_stime.tv_sec +
                    childusage.ru_stime.tv_usec / 1000000.0;

    printf("\nuser time = %g, sys time = %g\n", user, sys);

}

void SignInt(int signo)
{
  printf("SignInt\n");
  void pr_cpu_time();
  exit(0);
}

#endif  // K_UNIT_TEST_H_