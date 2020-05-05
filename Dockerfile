# 底层镜像依赖
FROM python:3.7
# 声明镜像作者
MAINTAINER "骆杨<ly@luoyangc.cn>"
# 设置时区
ENV TZ "Asia/Shanghai"

# 创建目录
RUN mkdir /blog
# 设置系统环境变量DOCKER_SRC
ENV DOCKER_SRC=blog
# 设置系统环境变量DOCKER_PROJECT
ENV DOCKER_PROJECT=/blog

# 切换工作目录
WORKDIR $DOCKER_PROJECT

# 将当前目录加入到工作目录中
ADD . $DOCKER_PROJEdockerCT

# 安装应用运行所需要的依赖
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 向外暴露端口
EXPOSE 8000

CMD ["sh", "start.sh"]