# blogging_platform

## Overview
a blogging platform allows users to create their own blogs and visit other's blogs.

built with flask framework and deployed to AWS-EC2.



## Result
website URL: http://ec2-54-168-200-241.ap-northeast-1.compute.amazonaws.com  

![](https://github.com/grass805/blogging_platform/blob/master/screenshot/screenshot1.jpg)
![](https://github.com/grass805/blogging_platform/blob/master/screenshot/screenshot2.jpg)
![](https://github.com/grass805/blogging_platform/blob/master/screenshot/screenshot3.jpg)


## Deployment
Amazon Linux AMI ec2-user


1. download the codes or git clone
```bash
~$ git clone git@github.com:grass805/blogging_platform.git

~$ cd blogging_platform
```

2. create a virtual environment (virtualenv) 
```bash
# enter root shell
~$ sudo su 

# with python3
~$ virtualenv VIRT --python=python3
```


3. overall directory structure
```
blogging_platform
|--VIRT
|--run.py             # to run the program
|--requirements.txt   # application dependencies
|--SharedBlog         # Flask application object
   |--__init__.py
   |--templates       # html files
   |--static          # CSS and JavaScript files
   |-- ......py
   |--blueprint       # Flask Blueprint object
      |--__init__.py
      |-- ......py
   
```

4. activate virtual environment
```bash
# activate virtual environment
~$ source VIRT/bin/activate
```

5. install python packages
```bash
~$ pip install -r requirements.txt
```



6. deployment

```bash
# run the application on port 80
~$ python run.py
```

```bash
*Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
```


## notice
if you want to keep the connection,

which means performing a long-running task on a remote machine,

plz run the process in a Screen session.

https://linuxize.com/post/how-to-use-linux-screen/


















