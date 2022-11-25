### 1 开发环境配置

#### 1.1 VS Code配置远程开发环境

如下图所示，直接在左端创建SSH远程连接即可。

![image-20221015205500124](https://qihang-1306873228.cos.ap-chongqing.myqcloud.com/imgs/image-20221015205500124.png)

#### 1.2 Git配置

1. 安装Git

   - 安装依赖库

     ```text
     yum install curl-devel expat-devel gettext-devel openssl-devel zlib-devel 
     ```

     ```bash
     yum install gcc-c++ perl-ExtUtils-MakeMaker
     ```

   - 下载源码包

     ```text
     cd /usr/src
     wget http://mirrors.edge.kernel.org/pub/software/scm/git/git-2.36.1.tar.gz
     ```

   - 解压、编译、安装

     ```bash
     tar -zxvf git-2.36.1.tar.gz
     cd git-2.36.1
     ./configure --prefix=/usr/local
     make
     make install
     ```

   - 刷新环境变量

     ```bash
     source /etc/profile
     ```

   - 查看git版本

     ```bash
     git --version
     ```

2. 运行`git config --global user.name "自己github的用户名"`设置用户名

3. 运行`git config --global user.email "自己github的邮箱"`设置邮箱

4. 在github中的个人设置界面新建SSH Keys并将`/home/hadoop/.ssh/id_rsa.pub`中内容粘入，保存即可。

   ![image-20221015193629335](https://qihang-1306873228.cos.ap-chongqing.myqcloud.com/imgs/image-20221015193629335.png)

5. 运行`git clone git@github.com:MineQihang/BigDataCourse.git`拉取仓库即可（此为私人仓库，需要先申请成为开发者）

6. 进入`lab2`文件夹再进行下一步

#### 1.3 Python配置（也可使用Anaconda配虚拟环境）

1. 更新pip

   ```shell
   sudo python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
   ```

2. 使用清华镜像

   ```shell
   sudo pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. 安装相关库

   ```shell
   sudo pip3 install -r requirements.txt
   ```

#### 1.4 安装字体文件

```shell
sudo yum install wqy-microhei-fonts
```

#### 1.5 安装驱动文件

1. 安装google-chrome

   ```shell
   sudo yum -y install google-chrome-stable
   ```

   > 如果找不到google-chrome-stable，请按照下方指令执行：
   >
   > 在目录 /etc/yum.repos.d/ 下新建文件 google-chrome.repo:
   >
   > ```
   > sudo vim /etc/yum.repos.d/google-chrome.repo
   > ```
   >
   > 写入如下内容:
   >
   > ```
   > [google-chrome]
   > name=google-chrome
   > baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
   > enabled=1
   > gpgcheck=1
   > gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
   > ```

2. 安装chromedrive

   chromedrive版本要和google-chrome对应，所以我们先查看google-chrome版本号：

   ```bash
   google-chrome-stable --version
   ```

   记录版本号后，去https://npm.taobao.org/mirrors/chromedriver/ 下载对应的驱动。**请修改下方的版本号**（如果没有，那么选择离本版本最近的即可）

   ```shell
   sudo rm -f chromedriver_linux64.zip*
   wget https://npm.taobao.org/mirrors/chromedriver/[版本号]/chromedriver_linux64.zip
   ```

   - 先删除之前的chromedriver

   ```shell
   sudo rm -f /usr/bin/chromedriver
   sudo rm -f /usr/local/bin/chromedriver
   sudo rm -f /usr/local/share/chromedriver
   ```

   - unzip 解压

   解压出文件chromedriver

   ```shell
   unzip chromedriver_linux64.zip
   ```

   - 赋予777权限

   ```shell
   chmod 777 chromedriver
   ```

   - mv 移动到/usr/bin/路径

   ```shell
   sudo mv chromedriver /usr/bin/
   ```

#### 1.6 设置日志级别

由于`spark` 在运行时会打印非常多的日志，为了便于调试观察，我们设置日志级别为 `WARN` 。

以下为全局设置日志级别方式，你也可在代码中临时设置 `sc.setLogLevel("WARN")`  （详见`ex3.pdf`）。

1. 切换到`conf` 目录

   ```bash
   cd /usr/local/spark/conf
   ```

2. 设置配置文件

   ```bash
   cp log4j.properties.template log4j.properties
   vim log4j.properties
   ```

   修改 `log4j.rootCategory=WARN,console`

### 2 编码WordCount.py



#### 2.2 提交到Spark运行

```
/usr/local/spark/bin/spark-submit /home/hadoop/BigDataCourse/lab2/WordCount.py 
```

![image-20221016105242523](https://qihang-1306873228.cos.ap-chongqing.myqcloud.com/imgs/image-20221016105242523.png)

# 遇到的问题

![image-20221015223453885](https://qihang-1306873228.cos.ap-chongqing.myqcloud.com/imgs/image-20221015223453885.png)

版本问题

换成Spark3.1.2

![image-20221016112512621](https://qihang-1306873228.cos.ap-chongqing.myqcloud.com/imgs/image-20221016112512621.png)

```
sudo chmod 777 BigDataCourse -R
```

设置权限即可



