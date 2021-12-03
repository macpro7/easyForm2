import sys 
sys.path.append("..") 
###################
#import requests
from flask import Flask,render_template,request,redirect,url_for

###################
import system.conf as s # --OR-- from system import conf
import util.OBJECTS as obj
from util.DATETIME import getDate
import db.sysDAO as sysd
from . import assist  as asst
import util.FILES as f


app = Flask(__name__,
    template_folder="../../webpage/",
    static_folder="../../webpage/static/",
    static_url_path="",
    ) #app = Flask("A")

app.config['SECRET_KEY'] = s.SECRET_KEY

#######------------------------------------------------------------###########
@app.template_filter()
def size(obj):
    return  len(obj) 
#######------------------------------------------------------------###########
@app.template_filter()
def getROLEKEY(objs):
    
    for one in objs:
        #print(one)
        if one.get("ROLE")=="KEY":
            return one["cont"]
    return ""

#######------------------------------------------------------------###########
@app.route('/subNewSimple/', methods = ['GET','POST'])
def subNewSimple():
    [LANG,UID,NextId,OBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID" )
    print(LANG,UID,NextId)
    msg=asst.SaveNewSimple(NextId,UID)
    ##

    NextId = s.RF_CONF.get(NextId).get("nextPageId")
    ##
    page=asst.basePageInfo(LANG,UID,NextId,OBJID)
    page.msg=msg
    
    return ToWorkPage(page,NextId,UID,LANG)

   
#######------------------------------------------------------------###########
def ToWorkPage(page,NextId,UUID,LANG):
    config=s.RF_CONF[NextId]
    table = asst.BuildListPage(config,page)
    page.ta=table

    return render_template( s.URLMAPPING[NextId][0],p=page)
#######------------------------------------------------------------###########
@app.route('/AddComment/', methods = ['POST'])
def AddComment():
    [LANG,UUID,NextId,OBJID,FOBJID,COBJID,textComment,questId ]= asst.BatchGetRequest(
        "la" , "UID" , "NextId" ,"OBJID","FOBJID","COBJID" ,"textComment","questId")

    print(LANG,UUID,NextId,OBJID,FOBJID,COBJID,textComment ,questId)
    asst.SaveComment( UUID,textComment,questId)
    page=asst.basePageInfo(LANG,UUID,NextId,OBJID,FOBJID,COBJID )
    

    return  ToRVVPage(page)
#######------------------------------------------------------------###########
@app.route('/work/', methods = ['GET','POST'])
def workRoute():
    [LANG,UID,NextId,OBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID"  )
    print(LANG,UID,NextId )
    page=asst.basePageInfo(LANG,UID,NextId,OBJID)
    page._dict=s.URLMAPPING
    ##

    return ToWorkPage(page,NextId,UID,LANG)
#######------------------------------------------------------------###########
@app.route('/CLOBJ/', methods = ['GET','POST'])
def CLOBJ():
    [LANG,UID,NextId,OBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID" )
    print(LANG,UID,NextId,OBJID )
    ##

    msg=asst.CloneSimple(NextId,OBJID,UID)
    
    ##
    CurrentId = NextId 
    NextId = s.RF_CONF.get(NextId).get("nextPageId")  
    page=asst.basePageInfo(LANG,UID,NextId,OBJID)
    ##
    
    page.msg=msg
    
    return ToWorkPage(page,NextId,UID,LANG)
#######------------------------------------------------------------###########

@app.route('/Quest/', methods = ['GET','POST'])
def Quest():
    [LANG,UUID,NextId,OBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID" )
    print(LANG,UUID,NextId,OBJID )
    page=asst.basePageInfo(LANG,UUID,NextId,OBJID)
    
    ##
    #page=asst.BuildComplexView(page,NextId,OBJID,LANG)
    return  ToTestPage(page)
#######------------------------------------------------------------###########
@app.route('/RVQ/', methods = ['GET','POST'])
def RVQ():
    #print("request.form" , request.form)
    [LANG,UUID,NextId,OBJID,FOBJID,COBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID","FOBJID","COBJID" )
    print(LANG,UUID,NextId,OBJID ,FOBJID,COBJID)
    page=asst.basePageInfo(LANG,UUID,NextId,OBJID,FOBJID,COBJID )
    
    ##
    #page=asst.BuildComplexView(page,NextId,OBJID,LANG)
    #return  ToRVPage(page)
    return  ToRVVPage(page)
#######------------------------------------------------------------###########
def ToRVVPage(p): 
    p.objlist=asst.BuildListPage(p.conf,p)
    return render_template("RVVIEW.htm",p=p)
#######------------------------------------------------------------###########
# @app.route('/NXQUEST/', methods = ['GET','POST'])
# def NXQUEST():
#     [LANG,UUID,NextId,OBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID" )
#     print(LANG,UUID,NextId,OBJID )
#     page=asst.basePageInfo(LANG,UUID,NextId)
    
#     ##
#     page=asst.BuildComplexView(page,NextId,OBJID,LANG)
#     return render_template( "CVIEW.htm",p=page)
#######------------------------------------------------------------###########
@app.route('/CKQUEST/', methods = ['GET','POST'])
def CKQUEST():
    [LANG,UUID,NextId,OBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID" )
    print(LANG,UUID,NextId,OBJID )
    page=asst.basePageInfo(LANG,UUID,NextId,OBJID)
    
    classObj = asst.getRequests2Class(NextId)

    if classObj.uuid == None or classObj.uuid == "" :
        pass
    else:
        asst.WriteObj(classObj)
        
    ##
    page=asst.BuildComplexView(page,NextId,OBJID,LANG)
    
    if page.doing==None or page.doing=="" or page.doing == 0:
        return ToTestPage(page)
    return render_template( "CVIEW.htm",p=page)

#######------------------------------------------------------------###########
@app.route('/CKOBJ/', methods = ['GET','POST'])
def CKOBJ():
    [LANG,UID,NextId,OBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID" )
    page=asst.basePageInfo(LANG,UID,NextId,OBJID)
    print(LANG,UID,NextId,OBJID )
    ##
    page=asst.constructViewSimpleUI(page,NextId,OBJID,LANG)
    return render_template( "View.htm",p=page)
#######------------------------------------------------------------###########
@app.route('/subEditSimple/', methods = ['GET','POST'])
def subEditSimple():
    [LANG,UID,NextId ,OBJID]= asst.BatchGetRequest( "la" , "UID" , "NextId","OBJID"   )
    print(LANG,UID,NextId)
    msg=asst.SaveEditSimple(NextId,UID)
    ##
    
   
    CurrentId = NextId
    NextId = s.RF_CONF.get(NextId).get("nextPageId")
    ##
    page=asst.basePageInfo(LANG,UID,NextId,OBJID)
    page.msg=msg

    return ToWorkPage(page,NextId,UID,LANG)

#######------------------------------------------------------------###########
@app.route('/EDOBJ/', methods = ['GET','POST'])
def EDOBJ():
    [LANG,UID,NextId,OBJID ]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID" )
    print(LANG,UID,NextId,OBJID)
    page=asst.basePageInfo(LANG,UID,NextId,OBJID)
    ##
    page=asst.constructViewSimpleUI(page,NextId,OBJID,LANG)
    return render_template( "editSimple.htm",p=page)
#######------------------------------------------------------------###########
@app.route('/newSimple/', methods = ['GET','POST'])
def newSimple():
    [LANG,UID,NextId ,OBJID]= asst.BatchGetRequest( "la" , "UID" , "NextId" ,"OBJID"  )
    page=asst.basePageInfo(LANG,UID,NextId,OBJID)
    print(LANG,UID,NextId )
    ##
    page=asst.constructNewSimpleUI(page,NextId,LANG)
    return render_template( "newSimple.htm",p=page)
#######------------------------------------------------------------###########
def ToTestPage(p): 
    p = asst.TestEntrance(p)
    return render_template("CLIST.htm",p=p)
#######------------------------------------------------------------###########
# def ToRVPage(p): 
#     obj list = asst.BuildListPage(p.conf,p)
#     p.obj list=objl ist
#     return render_template("RVLIST.htm",p=p)
#######------------------------------------------------------------###########

#######------------------------------------------------------------###########
def ToMainPage(p): 
    p._dict=s.URLMAPPING
    return render_template("Main.htm",p=p)
#######------------------------------------------------------------###########
@app.route('/auth/', methods = ['GET','POST'])
def auth():
    [LANG,loginId,authCode,OBJID ] = asst.BatchGetRequest( "la", "loginId"  ,  "authCode" ,"OBJID"  )
    p=asst.basePageInfo(LANG,"","",OBJID)
    user = sysd.getAuthByIDPS(loginId,authCode)
    if user==None:                                         ## authentication failure
        return ToLoginPage(p.T["i_loginfailed"],LANG)
    else:
        if user.validtill <= getDate(""):                  ## expired
            return ToLoginPage(p.T["i_user_expired"],LANG)
        if user.usertype == s.TEMP_USER_TYPE:              ## temp user page 
            p.userobj=user
            return ToTestPage(p)
        else:
            p.userobj=user                           ## admin / viewer page 
            return ToMainPage(p)
    return None

#######------------------------------------------------------------###########
###########################################################################################################
def ToLoginPage(msg,LANG):
    p=asst.basePageInfo(LANG,"","","")
    if msg!="":
        p.msg=msg
    p.code=f.getFileContent(s.FILE_PREFIX+s.FILE_MAPPING["loginpage"])
    return render_template("login.htm",p=p)
#######------------------------------------------------------------#######

###########################################################################################################

#######------------------------------------------------------------###########

 
#######------------------------------------------------------------###########
@app.route('/Tologin/', methods = ['GET','POST'])
def ToLogin():
    LANG=request.form.get("la")
    return ToLoginPage("",LANG)
#######------------------------------------------------------------###########
@app.route('/', methods = ['GET','POST'])
def preLogin():
    p=asst.basePageInfo("EN","","","")
    return render_template("preLogin.htm",p=p)
#######------------------------------------------------------------###########
@app.errorhandler(404)
def page_not_found(e):
    p=asst.basePageInfo("EN","","","")
    p.msg="Page Not Found"
    return render_template("preLogin.htm",p=p),404
@app.errorhandler(500)
def internal_server_error(e):
    p=asst.basePageInfo("EN","","","")
    p.msg="Error 500"
    return render_template("preLogin.htm",p=p),500
#######------------------------------------------------------------###########


