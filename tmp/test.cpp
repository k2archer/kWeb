
#include <python2.7/Python.h>
int main()
{
    //第一步：初始化Python
    //在调用Python的提供的给C的API之前，通过执行初始化
    //来添加Python的内建模块、__main__、sys等
    Py_Initialize();

    //检查初始化是否完成
    if (!Py_IsInitialized())
    {
        return -1;
    }

    //第二步：导入sys模块
    PyRun_SimpleString("import sys");

    //第三步：导入执行脚本时的命令行参数，如：./sample.py arg1 arg2
    PyRun_SimpleString("sys.argv['arg1','arg2']");

    //第四步：执行调用脚本文件命令,注意文件的路径
    if (PyRun_SimpleString("execfile('./sample.py')") == NULL)
    {
        return -1;
    }

    //第五步：关闭Python解释器
    Py_Finalize();
    return 0;
}