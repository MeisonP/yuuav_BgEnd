# README #


### What is this repository for? ###
* yuuav  server,  between user/client/front-end  and Locus 


* two flask app/ server: 
> 
1 front-end -->server  
> 
2 Locus image process info --->server
### 文件说明
* unit.py  contain many func that be called
* flaskapp_back2locus
> 
-------calling back2locus
> 
-------------------get_bbox2db
> 
-------------------get_xy2db

* flaskapp_front2back
> 
--------calling front2back
> 
-------------------time2bbox
> 
-------------------time2image

* extract_olddata:
> 
obtain all locus task info, and save it to database  to create the index table,


###业务逻辑
![image](https://bitbucket.org/Mason_P/yuuav_background_mason/raw/master/Architecture/structure.png)
