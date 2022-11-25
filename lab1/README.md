<h1 align='center'>实验一：环境搭建</h1>

## 0 准备工作

### 0.1 配置用户

该小节主要是创建`Hadoop` 用户。

1. 创建用户

   ```bash
   useradd -m hadoop -s /bin/bash          
   ```

   同时设置用户密码：（如 123456）

   ```bash
   passwd hadoop
   ```

2. 配置权限

   为了方便，给用户 `hadoop` 等同`root` 权限：

   ```bash
   visudo            # 执行 visudo命令进入vim编辑
   ```

   找到如下位置，添加红框那一行配置权限：

   ![1575371320579](https://blog-imgs-1256686095.cos.ap-guangzhou.myqcloud.com/1owVFrmRuLg2MCP.png)

3. 切换用户

   配置完成后，我们切换到hadoop用户下：

   ```bash
   su hadoop   # 注意，不要使用root用户，以下全部切换到hadoop用户下操作
   ```

   :warning: 如非特殊说明，**接下来所有命令都是Hadoop用户（不用使用root用户）下完成**！:warning: 

### 0.2 配置SSH

> 为什么要配置ssh？

因为集群、单节点模式都需要用到 ssh登陆。同时每次登陆ssh都要输入密码是件蛮麻烦的事 ，我们可以通过生成公钥配置来面密码登陆。

1. 生成密钥

   为了生成 ~/.ssh 目录，我们直接通过执行下面命令会直接生成

   ```bash
   ssh localhost   # 按提示输入yes，然后键入hadoop密码
   ```

   然后开始生成密钥

   ```bash
   cd ~/.ssh/          # 切换目录到ssh下
   ssh-keygen -t rsa   # 生成密钥
   ```

   生成密钥过程会有三个提示，不用管全部回车。

2. 授权

   ```bash
   cat id_rsa.pub >> authorized_keys  # 加入授权
   ```

3. 修改权限

   如果不修改文件`authorized_keys`权限为`600`，会出现访问拒绝情况

   ```bash
   chmod 600 ./authorized_keys    # 修改文件权限
   ```

4. 测试

   ```bash
   ssh localhost   # ssh登陆
   ```

   不用输入密码，直接登陆成功则说明配置正确。

   ![1579770536641](https://blog-imgs-1256686095.cos.ap-guangzhou.myqcloud.com/k5xYOtBjz3yZVmJ.png)

### 0.3 配置yum源

1. 切换到`yum` 仓库

   ```bash
   cd /etc/yum.repos.d/
   ```

2. 备份下原repo文件

   ```bash
   sudo mv CentOS-Base.repo CentOS-Base.repo.backup
   ```

3. 下载阿里云repo文件

   ```bash
   sudo wget -O /etc/yum.repos.d/CentOS-7.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   ```

   防止权限不足使用`sudo` 命令。

4. 设置为默认repo文件

   就是把阿里云repo文件名修改为 `CentOS-Base.repo` 

   ```bash
   sudo mv  CentOS-7.repo CentOS-Base.repo  # 输入y
   ```

5. 生成缓存

   ```bash
   yum clean all
   yum makecache
   ```

### 0.4 配置Java环境

*hadoop2* 基于 *java* 运行环境，所以我们先要配置*java* 运行环境。

1. 安装 JDK 

   执行下面命令，经过实际测试前面几分钟一直显示镜像错误不可用。它会进行自己尝试别的源，等待一会儿就可以下载成功了。

   ```bash
   sudo yum install java-1.8.0-openjdk java-1.8.0-openjdk-devel
   ```

   :warning: 此时默认安装位置是  `/usr/lib/jvm/java-1.8.0-openjdk` 

   其实，查找安装路径，可以通过以下命令：

   ```bash
   rpm -ql java-1.8.0-openjdk-devel | grep '/bin/javac'
   ```

   - `rpm -ql <RPM包名>` ：查询指定RPM包包含的文件
   - `grep <字符串>` ： 搜索包含指定字符的文件

2. 配置环境变量

   ```bash
   vim ~/.bashrc  # vim编辑配置文件
   ```

   在文件最后面添加如下单独一行（指向 JDK 的安装位置），并保存：

   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
   ```

   最后是环境变量生效，执行：

   ```bash
   source ~/.bashrc 
   ```

3. 测试

   ```bash
   echo $JAVA_HOME     # 检验变量值
   ```

   正常会输出 `2.`环境变量JDK配置路径。

   ```bash
   java -version
   ```

   正确配置会输出java版本号。

## 1 Hadoop单机版搭建

1. 下载

   > 为防止证书验证出现的下载错误，加上 `--no-check-certificate` ，相关讨论可见 [issue#1](https://github.com/Wanghui-Huang/CQU_bigdata/issues/1)

   ```bash
   sudo wget -O hadoop-2.10.2.tar.gz https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/stable2/hadoop-2.10.2.tar.gz  --no-check-certificate
   ```

   - `wget -O <指定下载文件名> <下载地址>` 

2. 解压

   ```bash
   sudo tar -zxf hadoop-2.10.2.tar.gz -C /usr/local
   ```

   把下载好的文件 `hadoop-2.10.2.tar.gz` 解压到 `/usr/local` 目录下

3. 修改文件

   ```bash
   cd /usr/local/   # 切换到解压目录下
   sudo mv ./hadoop-2.10.2/ ./hadoop      # 将加压的文件hadoop-2.10.2重命名为hadoop
   sudo chown -R hadoop:hadoop ./hadoop  # 修改文件权限
   ```

4. 测试

   ```bash
   cd /usr/local/hadoop     # 切换到hadoop目录下
   ./bin/hadoop version     # 输出hadoop版本号
   ```


## 2 Spark单机版搭建

1. 下载

   ```bash
   cd ~
   sudo wget -O spark-3.1.3-bin-without-hadoop.tgz http://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.1.3/spark-3.1.3-bin-without-hadoop.tgz
   ```

2. 解压

   同前解压到 `/usr/local` 目录下

   ```bash
   sudo tar -zxf spark-3.1.3-bin-without-hadoop.tgz -C /usr/local
   ```

3. 设置权限

   ```bash
   cd /usr/local   # 切换到解压目录
   sudo mv ./spark-3.1.3-bin-without-hadoop ./spark  # 重命名解压文件
   sudo chown -R hadoop:hadoop ./spark  # 设置用户hadoop为目录spark拥有者
   ```

4. 配置spark环境

   先切换到 `/usr/local/spark` ，（为了防止没权限，下面用`sudo`）

   ```bash
   cd /usr/local/spark
   cp ./conf/spark-env.sh.template ./conf/spark-env.sh
   ```

   编辑 `spark-env.sh` 文件 ：

   ```bash
   vim ./conf/spark-env.sh
   ```

   在第一行添加下面配置信息，使得Spark可以从Hadoop读取数据。

   ```
   export SPARK_DIST_CLASSPATH=$(/usr/local/hadoop/bin/hadoop classpath)
   ```

5. 配置环境变量

   ```bash
   vim ~/.bashrc
   ```

   在`.bashrc`文件中添加如下内容：

   ```python
   export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk  # 之前配置的java环境变量
   export HADOOP_HOME=/usr/local/hadoop    # hadoop安装位置
   export SPARK_HOME=/usr/local/spark   
   export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH           
   export PYSPARK_PYTHON=python3           # 设置pyspark运行的python版本
   export PATH=$HADOOP_HOME/bin:$SPARK_HOME/bin:$PATH
   ```

   最后为了使得环境变量生效，执行：

   ```bash
   source ~/.bashrc
   ```

6. 测试是否运行成功

   ```bash
   cd /usr/local/spark
   bin/run-example SparkPi
   ```

   执行会输出很多信息，也可以选择执行：

   ```bash
   bin/run-example SparkPi 2>&1 | grep "Pi is"
   ```

   ![1579771989587](https://blog-imgs-1256686095.cos.ap-guangzhou.myqcloud.com/DAvbtMa3HKoE1FW.png)

7. pyspark测试

   ```shell
   cd /usr/local/spark
   bin/pyspark
   ```

   





