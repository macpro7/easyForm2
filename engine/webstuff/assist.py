import sys 
sys.path.append("..") 
###################
from flask import request
###################
from db.sysDAO import getAll_CaseObj,query_misc_Dict,getTextbyLang,addObjectSimple,getAll_User                    # Methods
from db.sysDAO import query_Owners_Dict,UpdateObjectSimple,query_case_Dict,getObjByUUID,getAll_Question_Valid     # Methods
from db.sysDAO import getAll_Paper_Valid,UpdateLangTextObj,getCaseObj_UUID,getPaper_UUID ,getUserByUUID         # Methods
from db.sysDAO import query_paper_Dict,query_optionsCandidate_Dict,getQuestByUUID,deepClone,getRF_byAttr          # Methods
from db.sysDAO import getPaperName_UUID,getUser_UUID,getUserNamebyUUID,getRF_byFID,getFinishedUser    # Methods
#from db.sysDAO import                                   
from db.dbObjects import LangText,QustObj,User,RFObj,PaperObj,CaseObj,AnswerSheetObj # Objects


from db.cascadeQuery import getQuest_UUID_LANG_RF_ALL,getQuest_UUID_LANG_RF_TODO,get_QA_by_Paper_User
import system.conf as s # --OR-- from system import conf
import util.OBJECTS as obj
from util.UTI import dpcp,same,g,defaultFun,putUid,textGen
from util.DATETIME import getDate,getNowFull




CLASS_MAPPING={
    "newCaseId"    : CaseObj , 
                                            
    "EditCaseId"   : CaseObj ,   
    "CloneCaseId"  : CaseObj , 
        
        
    "newUserId"    : User,                                                    
    "EditUserId"   : User,      
    "CloneUserId"  : User,      
    
    "newPaperId"   : PaperObj,
    "EditPaperId"  : PaperObj,  
    "ClonePaperId" : PaperObj, 
                                            
    "newQuestId"   : QustObj,
    "EditQuestId"  : QustObj,
    "CloneQuestId" : QustObj,

    "lanObj"       : LangText,
    
    "questChkId"   : AnswerSheetObj ,

}

########-----------------------------------------------###############
def MakeLangText(reqlist):

    common=""
    for one in reqlist:
        if one.find(s.MULTI_LAN_SEP) > -1:
            para,lan= one.split(s.MULTI_LAN_SEP)
            common=para
            a=LangText()
            
            a.language = lan
            a.text = request.form.get( one )
            a.langcode = request.form.get( para )
            addObjectSimple(a)
    #  'paperNameId__EN', 'paperNameId__CH', 'paperNameId__JP'
    return common

########-----------------------------------------------###############
def UpdateLangText(reqlist):
    common=""
    for one in reqlist:
        if one.find(s.MULTI_LAN_SEP) > -1:
            para,lan= one.split(s.MULTI_LAN_SEP)
            common=para
            a=LangText()
            
            a.language = lan
            a.text = request.form.get( one )
            a.langcode = request.form.get( para )
            UpdateLangTextObj(a)
    #  'paperNameId__EN', 'paperNameId__CH', 'paperNameId__JP'
    return common
########-----------------------------------------------###############
def SaveNewSimple(NextId,UID):
    reqlist = UI2Requests(NextId)
    print("SaveNewSimple",  reqlist)
    if s.MULTI_LAN_MARK in reqlist:
        c = MakeLangText(reqlist)
    
    obj2save = SealRequestToClass(NextId ,reqlist)

    msg=addObjectSimple(obj2save)
    return msg
########-----------------------------------------------###############
def SaveEditSimple(NextId,UID):
    reqlist = UI2Requests(NextId)

    if s.MULTI_LAN_MARK in reqlist:
        c=UpdateLangText(reqlist)

    obj2save = SealRequestToClass(NextId ,reqlist)

    msg=UpdateObjectSimple( CLASS_MAPPING[NextId] ,obj2save)
    return msg

########-----------------------------------------------###############
def CloneSimple(NextId,OBJID,UID):
    oldObj = getObjByUUID( CLASS_MAPPING[NextId], OBJID ) 
    newObj = CloneObj(oldObj, NextId)
    msg=addObjectSimple(newObj)
    return msg
########-----------------------------------------------###############
def CloneObj(interfaceObj,NextId):# clone
    newObj =  {}
    steps= s.CLONE_PROCEDURE[NextId]
    
    ###
    #print(interfaceObj)
    
    for name,value in vars(interfaceObj).items():
        for line in steps:
            if line[0]==name:
                newObj[name] = value
    ##
    
    for line in steps:
        if line[1]!="":
            m,p = line[1].split(".")
            print(line[1])
            if m=="DEEPCOPY":
                newObj[line[0]]=FUNC_INVOKE[m](returnMemberOfClass(interfaceObj,p) , textGen("q") )
            elif m =="APPEND":
                newObj[line[0]]= newObj[line[0]]+ FUNC_INVOKE[m](p)
            else:
                newObj[line[0]]=FUNC_INVOKE[m](p)
        print(newObj)
    print("CloneObj.newObj  > " , newObj )
    
    ObjNew=CLASS_MAPPING[NextId]()
    ObjNew.__dict__.update(newObj)
    
    return ObjNew
########-----------------------------------------------###############
def sysTranverse(ori,page):
    #print("sysTranverse " , ori)
    if ori.find("$User_uuid")> -1:
        ori=ori.replace("$User_uuid",page.userobj.uuid)

    if ori.find("$lang") > -1:
        ori=ori.replace("$lang",page.T['LAN'])
    if ori.find("$P_OBJID") > -1:
        ori=ori.replace("$P_OBJID",page.OBJID  )
    if ori.find("$FOBJID") > -1:
        ori=ori.replace("$FOBJID",page.FOBJID  )
    if ori.find("$COBJID") > -1:
        ori=ori.replace("$COBJID",page.COBJID  )
    
    if ori.find("$")>-1:          
        if ori.find(".")>-1:
            func_name = ori[:ori.find(".")]
            param =ori[ori.find(".")+1:]
            # if param.find("$")>-1: 
            #     return FUNC_INVOKE[func_name](  param   ,page )
            # else:
            return FUNC_INVOKE[func_name](  param ,page)
            #print( "sysTranverse" , func_name )
            # "value": "$getNowFull.NOW",  must have 2 parts
        else:
            return ori ## let p_SIMPLE_UI to deal with 
                        # scenario :  "name": "owner",,"value": "$GET_UNAME", 
    else:
        return ori

########-----------------------------------------------###############
def ProcessFieldWithStar(stringCode,ObjInstance,LANG):
    
    #print( "ProcessFieldWithStar" , stringCode,"|",ObjInstance ,"\n")
    if stringCode.find("*") > -1:
        stringCode =stringCode[1:]
        field= returnMemberOfClass(ObjInstance,stringCode) 
        #print ( "*" , field )
        return getTextbyLang(LANG, field ).text ,stringCode
    else:
        field= returnMemberOfClass(ObjInstance,stringCode) 
        #print ( "!!*" , field ,",",stringCode)
        return field,stringCode
########-----------------------------------------------###############
def QueryValue_colCont(stringCode,ObjInstance,LANG):
    name=""
    #print("  >>>   ",stringCode)
    if stringCode.find(".") < 0 :
        if stringCode.find("*") < 0 :
            return  returnMemberOfClass(ObjInstance, stringCode) 
        else:
            #print("  >>>   ",stringCode)
            stringCode =stringCode[1:]
            stringCode=returnMemberOfClass(ObjInstance, stringCode) 
            return getTextbyLang(LANG,stringCode).text

    # "fid.getCase_UUID.case_name","cid.getUserByUUID.displayname","status.TS","uuid.OP" 
    
    requestName ,   Method_name , wantColumn =  stringCode.split(".") 
    
    #print("QueryValue_colCont" , Method_name )
    f,pc = FUNC_INVOKE[Method_name]
    if pc==1:
        pc=  returnMemberOfClass(ObjInstance, requestName) 
        instance_ = f(  pc  )

    if pc==2:
        pc=[returnMemberOfClass(ObjInstance, requestName)  ,LANG]
        instance_ = f(  pc  )
    
    if instance_ != None and instance_!="":
        name,stringCode= ProcessFieldWithStar(wantColumn, instance_, LANG)
 
        

    return name
########-----------------------------------------------###############
def BuildListPage(config,p):
    if  config.get("getList")==None :
        return []
    function_ = FUNC_INVOKE[config.get("getList")] 
    
    params= config["params"]
    trueParams=[]
    for a in params:
        cc=sysTranverse(a,p)
        trueParams.append(cc)
    #print(trueParams)
    objlist_original= function_(trueParams)
    
    if config.get("colCont")!=None:
        displayObjlist=[]
        for line in objlist_original:
            xline=[]
            for one in config["colCont"]:
                # originId,cmd,disName=one.split(".")
                name_=QueryValue_colCont(one,line,p.T["LAN"])
                xline.append(name_)
            displayObjlist.append(xline)
        return displayObjlist
    
    else:
        dicLine={}
        for line in objlist_original:
            key=""
            oneRecord=[]
            for one in config["data"]:
                one_field_item = FillDict(one)
                one_field_item["cont"]=QueryValue_from_cascadeQuery(one_field_item["cont"],line)
                one_field_item["pageCode"] = one_field_item["pageCode"].replace(
                    s.ANCHOR, one_field_item["cont"])
                
                one_field_item["pageCode"] = one_field_item["pageCode"].replace(
                    s.PREFIX, p.T[one_field_item["show"]]+" : ")
                
                
                if one_field_item.get("ROLE") == "KEY":
                    key= one_field_item["cont"]
                
                
                #print("\n..",one_field_item,"..\n")
                oneRecord.append(one_field_item)
            if dicLine.get(key)!=None:
                for newItem in oneRecord:
                    if newItem.get("ROLE")=="LIST":
                        dicLine[key].append(newItem)

    
            else:
                dicLine[key]=oneRecord
        # print("BuildListPage\n",displayObjlist)
        #print(dicLine)
        return dicLine
########-----------------------------------------------###############
def FillDict(confOne):
    a={}
    for c in confOne:
        a[c]=confOne[c]
    return a
########-----------------------------------------------###############
def QueryValue_from_cascadeQuery( stringCode , cascadeObjects):
    #print('QueryValue_from_cascadeQuery', stringCode)
    objOrder,objField = stringCode.split(".")
    objOrder=int(objOrder)
    return returnMemberOfClass(    cascadeObjects[objOrder]     ,objField    )
########-----------------------------------------------###############
def SaveComment( UUID,textComment,questId):
    obj = AnswerSheetObj()
    obj.uuid = g(32)
    obj.userId = UUID
    obj.questId = questId
    obj.answerCont = textComment
    obj.cDate = getNowFull()
    obj.created_by = UUID
    obj.attr = "COMMENT"
    obj.ans_type = "TEXT"
    obj.status =  "OK"
    addObjectSimple(obj)
    
    
    
########-----------------------------------------------###############
def select_param(ori_param , param_wanted):
    [page,NextId,OBJID,LANG] = ori_param
   
    ret=[]
    for one in param_wanted:
        ret.append(  sysTranverse(one,page)  )
    
    return ret
########-----------------------------------------------###############
def BuildComplexView(page,NextId,OBJID,LANG):
    params = [page,NextId,OBJID,LANG]
    TheFunc  = FUNC_INVOKE[   s.RF_CONF[NextId]["getView"]   ] # "getRFView"    : [ ComboFunc,3],
    # def getQuest_UUID_LANG_RF(params):
    #     user_uuid,lang = params
    page = TheFunc( s.RF_CONF[NextId]["getView"], params )  # "getRFView"    : [ ComboFunc,3],

    return page
########-----------------------------------------------###############
def ComboFunc(ID, params):
    [page,NextId,OBJID,LANG] = params
    #print("ComboFunc" , page,NextId,OBJID,LANG )
    result=[]
    final=""
    
    while ID !="":
        p_each = select_param(params, s.COMBO_FUNC[ID]["params"]   )
        TheFunc  = FUNC_INVOKE[   s.COMBO_FUNC[ID]["method"]   ]
        final= s.COMBO_FUNC[ID]["final"]
        
        result_process = s.COMBO_FUNC[ID]["result"] 
        if result_process == "len":
            result.append(  len(TheFunc( p_each ))      )
        if result_process == "count":
            result.append(  (TheFunc( p_each )).count() )
        
        else :
            result.append(  TheFunc( p_each ) )
        ID = s.COMBO_FUNC[ID]["next"] 
    

    f = FUNC_INVOKE[final]
    page = f(result,page)
    page = makePageInputData(NextId,page,result)
    return page 

########-----------------------------------------------###############
def resultList2Page(relist, page):   # getQuestFinal
    #print(relist[1].count())
    if relist[1]==None or relist[1]==[] or relist[1].count()==0 :
        page.doing=0
        page.msg='i_completed'
        return page
    else:
        #print("resultList2Page" , relist[1][0])
        pass
    page.total=relist[0]
    page.doing = page.total-relist[1].count() + 1
    page.percent = round( page.doing/page.total*100,0)
    page.currentQuest = relist[1][0][0].text
    page.currentQuestAnswerType = relist[1][0][1].answer_type   # LangText,QustObj,RFObj 
    page.option={}
    page.QuestId=relist[1][0][1].uuid
    if page.currentQuestAnswerType == "CHOICE":
        page.option=query_misc_Dict(relist[1][0][1].option_id)  # LangText,QustObj,RFObj 
    return page

########-----------------------------------------------###############
def makePageInputData(NextId,page,result):
    data_blueprint = s.RF_CONF[NextId]["data"]
    input_datas=[]
    for data_ in data_blueprint:
        ipd={}
        ipd["name"]=data_["name"]
        ipd["value"] = sysTranverse( data_["value"] , page)
        ipd["pageStyle"] = data_["pageStyle"]
        input_datas.append(ipd)
        
    
    page.data=input_datas
    #print(input_datas)
    
    return page
########-----------------------------------------------###############
def getRequestsGroupByUIdata(NextId):
    reqList=[]
    ilist = s.RF_CONF[NextId]['data']
 
    for line in ilist:
        reqList.append(line['name'])
    #print (reqList)
    return reqList
########-----------------------------------------------###############
def getRequests2Class (NextId):
    reqList = getRequestsGroupByUIdata(NextId)
    classObj = SealRequestToClass(NextId , reqList)
    return classObj
########-----------------------------------------------###############
def WriteObj(obj):
    addObjectSimple(obj)
########-----------------------------------------------###############
def basePageInfo(LANG,UUID,NextId,OBJID,FOBJID="",COBJID=""):
    p=obj.pageInfo()
    p.setVersion(s.VERSION)
    p.initText(getTextbyLang(LANG))
    ##
    p.userobj = getUser_UUID(UUID)
    p.OBJID=OBJID
    p.FOBJID=FOBJID
    p.COBJID=COBJID
    ##
    p.conf=s.RF_CONF[NextId]
    p.NextId=NextId
    return p
########-----------------------------------------------###############
def TestEntrance(p):
    config = s.RF_CONF["QuestMain"]

    objlist = BuildListPage(config,p)

    p.objlist=objlist
    p.conf = config

    return p

########-----------------------------------------------###############
def getFromPage(key,page):
    #print("getFromPage >>" , key, page)
    return returnMemberOfClass(page,key)
    
########-----------------------------------------------###############
def UI2Requests(NextId):
    reqList=[]
    ui=dpcp(s.RF_CONF[NextId]["data"])
    #print(ui)
    for line in ui:
        for mark in s.Request_MARK:
            if line.get("name").find(mark) > -1:
                line["name"] = line.get("name").split(mark)[0]
        reqList.append(line.get("name"))
    #print (reqList)
    return reqList
########-----------------------------------------------###############
def selectFunc(NextId,KEYID, objType=None , ifValid=None ):
    print ("selectFunc ",NextId,KEYID)
    if objType == None :
        if  ifValid==None:
            objs = FUNC_INVOKE[NextId](KEYID)

        else:
            pass #######################################################
    else :
        if ifValid==None:
            objs = FUNC_INVOKE[NextId](objType,KEYID)
        else:
            objs = FUNC_INVOKE[NextId](objType,KEYID,ifValid)
    return objs
########-----------------------------------------------###############
########-----------------------------------------------###############  
def returnMemberOfClass(classInstance,memberName):
    if memberName == "COUNT":
        #print(classInstance.count())
        return classInstance.count()
    if memberName == "ORI":
        #print(classInstance)
        return classInstance
    if memberName == "LEN":
        #print(classInstance)
        return len(classInstance)
    if memberName == "OBJ":
        #print(classInstance)
        return classInstance
    #print( "returnMemberOfClass ",  memberName  )
    if memberName.find(".")>-1:
        memberName=memberName[:memberName.find(".")]
        
    for name,value in vars(classInstance).items():
        if memberName==name:
            return value
        
    return ""
########-----------------------------------------------###############

########-----------------------------------------------###############

def ProcessMultiLanguage(requestName,OBJ):
    name=requestName
    lan=""
    name,lan =requestName.split(s.MULTI_LAN_SEP)
    print(name, lan)
    value = returnMemberOfClass(OBJ, name ) 
    value = getTextbyLang(lan,value).text
    return value
    

         
    
########-----------------------------------------------###############

########-----------------------------------------------###############
def p_SIMPLE_UI(NextId,LANG,page,OBJ  ): ## # scenario : "data" : [ . . . ] 
   
    conf = s.RF_CONF[NextId]
    fields = conf["data"]
    pageMembers=dpcp(fields)
    for i in range ( len(pageMembers)  ):
        pageMembers[i]["value"] = sysTranverse(pageMembers[i].get("value"),page)
        ##########
        if OBJ != None:
            
            if pageMembers[i].get("name").find(s.MULTI_LAN_SEP) > -1:
                pageMembers[i]["value"] =  ProcessMultiLanguage(pageMembers[i].get("name"),OBJ)
            else:
                value = returnMemberOfClass(OBJ,pageMembers[i].get("name")  )
                #print("------",value)
                if pageMembers[i].get("value").find("$") >-1 :    
                    print("pageMembers[i].get(value) > 1 ",pageMembers[i].get("value"))
                                            # scenario :  "name": "owner",,"value": "$GET_UNAME", 
                    value = FUNC_INVOKE[pageMembers[i].get("value")](value,page) 
                if pageMembers[i].get("value").find("*") >-1 : 
                    value,str_code = ProcessFieldWithStar(pageMembers[i].get("value"),OBJ,LANG)
                pageMembers[i]["value"] =  value
                #print( pageMembers[i]["value"] )

        pageMembers[i]["sub"] = extractGeneratingMethod( pageMembers[i].get("sub"),page )
        ##########
        print(pageMembers[i])
    return pageMembers
########-----------------------------------------------###############
########-----------------------------------------------###############
def extractGeneratingMethod( method_param ,page  ):
    if method_param == None:
        return ""
    if method_param.find("$lang") > -1:
        method_param=method_param.replace("$lang",page.T['LAN'])
    method=method_param
    param=""
    if method_param.find(".")>-1:
        method,param = method_param.split(".")
    return selectFunc(method,param)
########-----------------------------------------------###############
def constructNewSimpleUI(page,NextId,LANG):
    OBJ=None
    config_view=p_SIMPLE_UI(NextId,LANG,page,OBJ  )
    page.UI=config_view
    return page
########-----------------------------------------------###############


########-----------------------------------------------###############

########-----------------------------------------------###############

########-----------------------------------------------###############
def constructViewSimpleUI(page,NextId,OBJID,LANG):
    page.title=NextId
    OBJ=None
    print( "constructViewSimpleUI : ",NextId ,s.RF_CONF[NextId]['getView'] )
    f,pc = FUNC_INVOKE[s.RF_CONF[NextId]['getView']]
    
    if pc==1:
        OBJ = f(  OBJID  )
    #print(OBJ)   

    if OBJ != None:
        page.viewObj= p_SIMPLE_UI(NextId,LANG,page,OBJ  )
    else:
        page.viewObj=None
    return page


########-----------------------------------------------###############
########-----------------------------------------------###############


########-----------------------------------------------###############

########-----------------------------------------------###############

########-----------------------------------------------###############
def SealRequestToClass(nextId , parameters):
    #print( nextId , parameters)
    iclass= CLASS_MAPPING[nextId]()
    d={}
    for one in parameters:
        req_value =request.form.get(one)
        d[one]=req_value
    ##
    if d.get('answerCont_exp') !=None and d.get('answerCont_exp') !="":
        d['answerCont']=d['answerCont']+" "+d['answerCont_exp']+":00"
    ##
    iclass.__dict__.update(d)
    return iclass
########-----------------------------------------------###############

########-----------------------------------------------###############
def BatchGetRequest(*parameters):
    return_value=[]
    for one in parameters:
        a=request.form.get(one)
        return_value.append(a)
    return return_value
########-----------------------------------------------###############

########-----------------------------------------------###############

########-----------------------------------------------###############

########-----------------------------------------------###############
#######################################################################################


########-----------------------------------------------###############
    # elif stringCode.find("*") > -1:
    #     return ProcessFieldWithStar(stringCode,ObjInstance,LANG)
        
    #     # stringCode =stringCode[1:]
    #     # field= returnMemberOfClass(ObjInstance,stringCode) 
    #     # return getTextbyLang(LANG, field ).text ,stringCode
    # # elif stringCode.find("^") > -1:
    # #     return PagePreProcess(stringCode,ObjInstance ) ,stringCode[:stringCode.find("^")]
    # else:
    #     field= returnMemberOfClass(ObjInstance,stringCode)
    #     return  field,stringCode
########-----------------------------------------------###############

########-----------------------------------------------###############
# def PagePreProcess(cmdString,ObjInstance): #"paperNameId__EN^lanObj^text^getLangText"
#     returnValue=""
#     requestName,param2,methods = cmdString.split("^")

#     reqComm,lan =requestName,""
#     if requestName.find(s.MULTI_LAN_SEP) > -1:
#         reqComm,lan =requestName.split(s.MULTI_LAN_SEP)
#         lanObjInstance = FUNC_INVOKE[methods](lan,  returnMemberOfClass(ObjInstance, reqComm)    )
#         if lanObjInstance!=None and lanObjInstance!="":
#             returnValue = returnMemberOfClass(lanObjInstance, param2)
#     else:
#         pass
    
#     return returnValue
########-----------------------------------------------###############

FUNC_INVOKE = {
    "mainpage"      : print ,        


    # "EditCaseId"    : getCaseObj_UUID,        


    # "EditPaperId"   : getPaper_UUID, 
    
  
    #"EditQuestId"   : getQuestByUUID,
    ############
   # "getLangText"   : getTextbyLang,  
    
    #"getPaperByUUID": getPaper_UUID,
    ############
    ############
    "getFinishedUser" : [getFinishedUser,2],
    "getAssigned_FID" : [getRF_byFID,2],
    "getCasebyUUID" : [getCaseObj_UUID,1],
    "getPaper_UUID" :  [getPaper_UUID,1],
    "getUser_UUID" :  [ getUser_UUID,1],
    #"TS"           :  [ getText_langcode,2],
    #"OP"           : [ same,1],
    "GET_USER"    :  [getUserByUUID,1],
    "getQuestByUUID" : [getQuestByUUID,1],
    ############
    "getRFView"    : ComboFunc,
    "getQuestALL"  : getQuest_UUID_LANG_RF_ALL,
    "getQuestTodo" : getQuest_UUID_LANG_RF_TODO,
    "getQuestFinal": resultList2Page,
    "getRF"        : getRF_byAttr,
    ############
    ############
    "$g"         : g,              # $g.32
    "$getFromPage" : getFromPage, #   $getFromPage.currentQuestAnswerType
    "$GET_UNAME"   : getUserNamebyUUID, #$GET_UNAME
    "$GET_PAPERNAME" : getPaperName_UUID, #$GET_PAPERNAME
    
    
    ############
    ############
    "getAll_User"           : getAll_User,
    "getAll_CaseObj"        : getAll_CaseObj,
    "getAll_Paper_Valid"    : getAll_Paper_Valid,  
    "getAll_Question_Valid" : getAll_Question_Valid,
    "get_QA_by_Paper_User" : get_QA_by_Paper_User,
    "DEEPCOPY"              : deepClone,  #DEEPCOPY.paperNameId
    ############

    ############
   
    "APPEND"  : same,        # APPEND._CLONED
    ""        : defaultFun,
    "$AUTODATE": getDate,    # AUTODATE.NOW
    "$AUTODT"  : getNowFull, #$AUTODT.NOW
    
    
    ### "sub":METHOD
    "MISC"    : query_misc_Dict,
    
    
    "CASES"   : query_case_Dict,
    "PAPERS"  : query_paper_Dict,
    "USER"    : query_Owners_Dict,
    "OPTION"  : query_optionsCandidate_Dict,
    "HIDDEN"  : same,
    "TEXT"    : same,
    "SSELECT" : same,
    "OPTIONS" : same,
    

    "Default" : same,   # Default.DISABLED
    #"DATE"    : same,
   
  
    "$TEXTGEN" : textGen,  # $TEXTGEN.q
}

# findValueByClassAndMember
# sysTranverse
# ProcessFieldWithStar