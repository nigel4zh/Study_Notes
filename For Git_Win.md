#### 01 安装客户端

#### 02 设置账户
```
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
```

#### 03 SSH公钥授权
1. Git Bash下`ssh`确认已经安装SSH
2. `ssh-keygen -t rsa`，然后连续几个回车，生成文件及目录在`username/.ssh`下
3. 将`id_rsa.pub`的内容添加到GitHub账号上

#### 04 创建本地版本库
1. 进入目录下，`mkdir 目录名`创建空目录
2. `git init`创建版本库

#### 05 添加远程仓库
`git remote add origin git仓库地址`

#### 6 更新版本库到本地
`git pull origin master`

#### 07 提交本地项目
1. `git add 文件名`提交文件到暂存区
2. `git commit -m"本次提交说明“`提交更改
3. `git push origin master`将更改推送到服务器
