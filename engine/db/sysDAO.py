import sys


sys.path.append("..")
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime ,text
from sqlalchemy.orm import sessionmaker


##############################
# import CONF as C
# import TOOLS as T
from db.dbObjects import LangText,QustObj,User,RFObj,PaperObj,MiscListObj,CaseObj,AnswerSheetObj
from system import conf as C

# case
#  |- paper --> for different department / assign different users
#       |- topic --> group of questions
#            |- question --> TYPE : BLOCK / TABLE / ...
#                  |- part --> part of question
#

##  user <----> paper 

# all cont should be linked to t_lang

## question   : question_id(uuid), question_no , question_cont, answer_type , option_id(if option) , attributes ,  iftemplate , ifvalid,  created_datetime, created_by
## part       : uuid, question_id , part_no,  part_cont , part_type (title/ table_column / text / ... ) , option_id( if table column / if option / if table) ,attributes
## table_     : uuid , question_id, talbe_title , iftemplate , ifvalid,  created_datetime, created_by
## table_col  : uuid , table_.uuid , col_no , col_name , col_type , 

## answer     : uuid , part.uuid , answer_id , answer_type , answer_content , option_id(if option) , answer_datetime , answer_by ,attributes 


## ScoreBasis : 

Base = declarative_base()
engine = create_engine(C.DB, echo=False, connect_args={"check_same_thread": False})


def init_db():
    Base.metadata.create_all(engine)


##---------------------------------------------------##
##---------------------------------------------------##

##############################################################################################################
def deepClone(langcode,gen_code):
    #print(langcode,gen_code)
    langs=["CH","EN","JP"]
    dic={}
    for lanType in langs:
        dic[lanType] =  getTextbyLang(lanType, langcode).text
    
    for aa in dic:
        new_text = LangText()
        new_text.langcode = gen_code
        new_text.language = aa
        new_text.text= dic[aa]
        #print(new_text)
        addObjectSimple(new_text)
    return gen_code
##---------------------------------------------------##
def getRF_byAttr(params):
    #print(params)
    uid,attr=params
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    ones=(session.query(RFObj).filter( RFObj.cid==uid,  RFObj.attribute == attr )) 
   # print (ones.count())
    return ones
##---------------------------------------------------##
def getRF_byFID(params):
    #print("getRF_byFID",params)
    [fid,*_]=params
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    ones=(session.query(RFObj).filter( RFObj.fid==fid,  RFObj.attribute == "PAPER_USER" ,RFObj.status == "OPEN" )) 
    #print (ones.count())
    return ones
##---------------------------------------------------##
def getCount_bySQL(sql):
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    a=session.execute(text(sql)).fetchall()
    session.close()
    return a[0]
##---------------------------------------------------##
def getALL_bySQL(sql):
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    a=session.execute(text(sql)).fetchall()
    session.close()
    return a
##---------------------------------------------------##
def getFinishedUser( params ):
    [fid,*_]=params
    
    sql = "select count(1) from  qust_obj q "
    sql=sql + " where q.paperId  = '"+fid+"'"
    count = getCount_bySQL(sql)[0]
    
    sql = "select userId,count(1) as c from answersheet_obj a , qust_obj q "
    sql=sql + " where a.questId  = q.uuid and q.paperId = '"+fid +"'" 
    sql=sql + " group by userId "
    
    members = getALL_bySQL(sql)
    #print(members)
    #counted=[]
    usr=[]
    for one in members:
        #print(count,one[1],one[0])
        if one[1] == count:
            #counted.append(one)
            #print(one[0])
            a=getUserByUUID(one[0], ifValid=None)
            #print(a.uuid)
            usr.append(a)
    #print( "getFinishedUser" , type(usr))
    return usr
    
##---------------------------------------------------##

##---------------------------------------------------##
def getTextbyLang(lanType, langcode=None):
    #print(  "getTextbyLang" ,  lanType, langcode)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    re = dict()
    if langcode == None:
        ones = session.query(LangText).filter(LangText.language == lanType)
        for one in ones:
            # print(one)
            re[one.langcode] = one.text
        return re
    else:
        ones = session.query(LangText).filter(
            LangText.language == lanType, LangText.langcode == langcode
        )
        if ones.count() > 0:
            return ones[0]
        else:
            return ""
##---------------------------------------------------##
# def getText_langcode(para):
#     lanType, langcode=None,None
#     if isinstance(para,str)==True:
#         lanType=para
#     if isinstance(para,list)==True:
#         [lanType, langcode]=para
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     re = dict()
#     if langcode == None:
#         ones = session.query(LangText).filter(LangText.language == lanType)
#         for one in ones:
#             # print(one)
#             re[one.langcode] = one.text
#         return re
#     else:
#         ones = session.query(LangText).filter(
#             LangText.language == lanType, LangText.langcode == langcode
#         )
#         if ones.count() > 0:
#             return ones[0]
#         else:
#             return ""

##---------------------------------------------------##

##---------------------------------------------------##

##---------------------------------------------------##
def getAuthByIDPS(loginId, pswd):
    ulist = []
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = session.query(User).filter(User.login_id == loginId, User.login_pass == pswd)
    re = dict()
    for one in ones:
        ulist.append(one)
    # print(ulist)
    if len(ulist) == 0:
        return None
    else:
        return ulist[0]

##---------------------------------------------------##

##---------------------------------------------------##
def getCaseObj_UUID(uuid):
    #print("getCaseObj_UUID", uuid )
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = session.query(CaseObj).filter(CaseObj.uuid == uuid)
    if ones.count() > 0:
        return ones[0]
    else:
        return None
##---------------------------------------------------##
def getPaperName_UUID(uuid,p):
    #print(p.T['LAN'])
    id= getPaper_UUID(uuid).paperNameId
    return getTextbyLang(p.T['LAN'],id).text
    
##---------------------------------------------------##   
def getPaper_UUID(params):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ################
    uuid=None
    ifValid=None
    #print(params)
    
    ################
    if isinstance(params,str) ==True:
        uuid=params
        ones = session.query(PaperObj).filter(PaperObj.uuid == uuid)
        if ones.count() > 0:
            return ones[0]

    elif isinstance(params,list) ==True:
        uuid,ifValid=params
        ones = session.query(PaperObj).filter(
            PaperObj.uuid == uuid, PaperObj.case_status == ifValid
        )
        if ones.count() > 0:
            return ones[0]
    
    else:
        return None
##---------------------------------------------------##
def getQuestByUUID(uuid, ifValid=None):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if ifValid == None:
        ones = session.query(QustObj).filter(QustObj.uuid == uuid)
    else:
        ones = session.query(QustObj).filter(
            QustObj.uuid == uuid, QustObj.ifValid == ifValid
        )

    if ones.count() > 0:
        return ones[0]
    else:
        return None

##---------------------------------------------------##
def getUserNamebyUUID(uuid,param):
    print("getUserNamebyUUID", uuid )
    if getUserByUUID(uuid,None)!=None:
        return getUserByUUID(uuid,None).displayname
    else:
        return "-"

##---------------------------------------------------##
def getUserByUUID(uuid, ifValid=None):
    # print("getUserByUUID " , uuid)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if ifValid == None:
        ones = session.query(User).filter(User.uuid == uuid)
    else:
        ones = session.query(User).filter(User.uuid == uuid, User.ifValid == ifValid)
    #print( ones.count())
    if ones.count() > 0:
        return ones[0]
    else:
        return None

##---------------------------------------------------##
def getUser_UUID(pa):
    uuid, ifValid=None,None
 
    if isinstance(pa,str)==True:
        uuid=pa
    if  isinstance(pa,list)==True:
        uuid, ifValid=pa
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if ifValid == None:
        ones = session.query(User).filter(User.uuid == uuid)
    else:
        ones = session.query(User).filter(User.uuid == uuid, User.ifValid == ifValid)

    if ones.count() > 0:
        return ones[0]
    else:
        return None
##---------------------------------------------------##
def getObjByUUID(obj_class, uuid, ifValid=None):

    print("getObjByUUID : ---->")
    #print((obj_class), type(obj_class), uuid, ifValid)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if ifValid == None:
        ones = session.query(obj_class).filter(obj_class.uuid == uuid)
    else:
        ones = session.query(obj_class).filter(
            obj_class.uuid == uuid, obj_class.ifValid == ifValid
        )

    if ones.count() > 0:
        return ones[0]
    else:
        return None
    return None


##---------------------------------------------------##
def getAll_User(user_type):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = session.query(User)
    # if user_type == "":
    # else:
    #     ones=(session.query(User).filter(   User.usertype ==user_type  ))
    # for one in ones:
    #     print('getAll_User : ',one)
    return ones


##---------------------------------------------------##
def getAll_Paper_Valid(uuid):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = session.query(PaperObj).filter(PaperObj.ifvalid == "YES")
    return ones
##---------------------------------------------------##
def getAll_Question_Valid(uuid):
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    ones=(session.query(QustObj).filter(   QustObj.ifvalid == "YES" )) 
    return ones
##---------------------------------------------------##

##---------------------------------------------------##
def getAll_CaseObj(_owner):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = session.query(CaseObj)
    # if _owner == "":
    #     ones=(session.query(CaseObj))
    # else:
    #     ones=(session.query(CaseObj).filter(   CaseObj.owner ==_owner  ))
    return ones
##---------------------------------------------------##
def saveComment(UUID,text):
    pass
##---------------------------------------------------##
def getAnswerbyUUID(UUID):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = session.query(AnswerSheetObj)

    return ones
##---------------------------------------------------##
def addObjectSimple(obj):
    try:
        DBSession = sessionmaker(bind=engine)
        ss = DBSession()
        ss.add(obj)
        ss.flush()
        ss.commit()
        print(">> addObjectSimple completed : ")
        return "msg_Successful"
    except (Exception) as e:
        print("addObjectSimple Error : ", e)
        return "msg_Failed"


##---------------------------------------------------##
def UpdateObjectSimple(class_type, obj):
    try:
        DBSession = sessionmaker(bind=engine)
        ss = DBSession()
        ss.query(class_type).filter(class_type.uuid == obj.uuid).delete(
            synchronize_session=False
        )
        ss.flush()
        ss.commit()

        addObjectSimple(obj)

        print(">> UpdateObjectSimple completed : ")
        return "msg_Successful"
    except (Exception) as e:
        print("UpdateObjectSimple Error : ", e)
        return "msg_Failed"


##---------------------------------------------------##
def UpdateLangTextObj(lanObj):
    try:
        DBSession = sessionmaker(bind=engine)
        ss = DBSession()
        ss.query(LangText).filter(
            LangText.language == lanObj.language, LangText.langcode == lanObj.langcode
        ).delete(synchronize_session=False)
        ss.flush()
        ss.commit()

        addObjectSimple(lanObj)

        return "msg_Successful"
    except (Exception) as e:
        print("UpdateObjectSimple Error : ", e)
        return "msg_Failed"


##---------------------------------------------------##
def query_misc_by_cata(mcata):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = (
        session.query(MiscListObj)
        .filter(MiscListObj.mcata == mcata, MiscListObj.ifvalid != "0")
        .order_by(MiscListObj.ifvalid.asc())
    )
    return ones


##---------------------------------------------------##

##---------------------------------------------------##
def query_Owners(NOT_VALUE):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = session.query(User).filter(User.usertype != NOT_VALUE)
    return ones


##---------------------------------------------------##
def query_Owners_Dict(NOT_VALUE):
    objs = query_Owners(NOT_VALUE)
    ones = {}
    for i in objs:
        ones[i.uuid] = i.displayname
    return ones


##---------------------------------------------------##
def query_misc_Dict(mcata):
    ones = {}
    objs = query_misc_by_cata(mcata)
    # print(">>>>>>>>>>>>>",mcata,objs.count())
    for i in objs:
        ones[i.mtext] = i.mtext

    return ones


##---------------------------------------------------##
def query_case_Dict(_owner):
    ones = {}
    objs = getAll_CaseObj(_owner)
    # print(">>>>>>>>>>>>>",mcata,objs.count())
    for i in objs:
        ones[i.uuid] = i.case_name
    return ones
##---------------------------------------------------##
def query_paper_Dict(lanType):
    ones = {}
    objs = getAll_Paper_Valid("")
    for i in objs:
        case = getTextbyLang(lanType, langcode=i.paperNameId )
        ones[i.uuid] =  case.text
    return ones
##---------------------------------------------------##
def query_optionsCandidate_Dict(likeword):
    ret={}
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    ones = (
        session.query(MiscListObj)
        .filter(MiscListObj.mcata.like('%'+likeword+'%' ) , MiscListObj.ifvalid != "0")
        .order_by(MiscListObj.mcata.asc())
    )
    A=[]
    for one in ones:
        a=[]
        a.append(one.mcata)
        a.append(one.mtext)
        A.append(a)
 

    for xx in range (len(A)):
         for yy in range (len(A)):
            if A[xx][0] == A[yy][0] and A[xx][1] != A[yy][1]:
                A[xx][1] = A[xx][1]+ "/"+A[yy][1]
                A[yy][0]=""
                A[yy][1]=""
    for a in A:
        if a[0]!="":
            ret[a[0]]=a[1]

    return ret
##---------------------------------------------------## 
    
    
    
#def query_with_lang_tag_Dict(obj_type,keyFieldName):
    

##---------------------------------------------------##

##---------------------------------------------------##
#init_db()


# #########################################################################################


# def countAll():
#     DBSession = sessionmaker(bind=engine)
#     session=DBSession()
#     print(session.query(func.count(UserObj.id)).scalar())


# def query_All():
#     DBSession = sessionmaker(bind=engine)
#     session=DBSession()
#     ones=(session.query(UserObj).filter(   UserObj.valid >- 10,UserObj.modifiedby !='0' ).order_by(UserObj.valid.desc()))
#     #for one in ones:
#         #p rint(one)
#     return ones


# def sealUser(genid_,schema_id_,valid_,User_name_,login_id_,login_pass_,User_mobile_,User_mail_,status_,modifiedby_,modifieddatetime_):
#     u=UserObj()
#     u.genid = genid_
#     u.schema_id = schema_id_
#     u.valid = valid_
#     u.User_name = User_name_
#     u.login_id = login_id_
#     u.login_pass = login_pass_
#     u.User_mobile = User_mobile_
#     u.User_mail = User_mail_
#     u.status = status_
#     u.modifiedby = modifiedby_
#     u.modifieddatetime = modifieddatetime_
#     return u
# #########################################################################################
# def getUserByUID(_uid):
#     if _uid==None or len(_uid)<1:
#         return None
#     DBSession = sessionmaker(bind=engine)
#     session=DBSession()
#     ones=(session.query(UserObj).filter(   UserObj.valid == 1, UserObj.genid == _uid ))
#     try:
#         return ones[0]
#     except:
#         return None

# def getUserByUIDwhateverValid(_uid):
#     if _uid==None or len(_uid)<1:
#         return None
#     DBSession = sessionmaker(bind=engine)
#     session=DBSession()
#     ones=(session.query(UserObj).filter(   UserObj.genid == _uid ))
#     try:
#         return ones[0]
#     except:
#         return None

# def updateUsersSchema(_uid,sch):
#     t0=T.getTime_L()
#     old_=getUserByUID(_uid)
#     if old_.schema_id.find(sch)>-1:
#         print("No need to update user's schema.")
#         return

#     if len(old_.schema_id)<2:
#         new_=sch
#     else:
#         new_=old_.schema_id+","+sch

#     DBSession = sessionmaker(bind=engine)
#     session=DBSession()

#     session.query(UserObj).filter( UserObj.genid == _uid ,UserObj.valid == 1  ).update({UserObj.schema_id:new_    })
#     session.flush()
#     session.commit()
#     print('>> updateUsersSchema completed : '+ str(T.getTime_L()-t0))


# def updateUsersValid(_uid,valid_int):
#     t0=T.getTime_L()
#     try:
#         DBSession = sessionmaker(bind=engine)
#         session=DBSession()

#         session.query(UserObj).filter( UserObj.genid == _uid   ).update({UserObj.valid:valid_int    })
#         session.flush()
#         session.commit()
#         print('>> updateUsersValid completed : '+ str(T.getTime_L()-t0))
#     except(Exception) as e:
#         print("updateUsersValid ",e)

# def updateUserObjbyId(usr):
#     t0=T.getTime_L()
#     try:
#         DBSession = sessionmaker(bind=engine)
#         session=DBSession()
#         session.query(UserObj).filter( UserObj.genid == usr.genid   ).update(
#             {
#                 UserObj.valid:usr.valid,
#                 UserObj.User_name : usr.User_name,
#                 UserObj.login_id : usr.login_id,
#                 UserObj.login_pass : usr.login_pass,
#                 UserObj.User_mobile : usr.User_mobile,
#                 UserObj.User_mail : usr.User_mail,
#                 UserObj.status : usr.status,
#                 UserObj.modifiedby : usr.modifiedby,
#                 UserObj.modifieddatetime : usr.modifieddatetime
#             }
#             )
#         session.flush()
#         session.commit()
#         print('>> updateUserObjbyId completed : '+ str(T.getTime_L()-t0))
#     except(Exception) as e:
#         print("updateUserObjbyId ",e)


# def getUserByMobile(mo):
#     if mo==None or len(mo)<11:
#         return None
#     #p rint(mo,"MO")
#     DBSession = sessionmaker(bind=engine)
#     session=DBSession()
#     ones=(session.query(UserObj).filter(   UserObj.valid == 1, UserObj.User_mobile == mo ))
#     return ones[0]


# # updateUsersSchema("76b1cbf7d4106a85","a3c421f155bd2930138fafebf13ba16f")
# # def packageAndAddOrder(ord):
# #     l=[]
# #     l.append(ord)
# #     addOrders(l)
# #     countAll()

# # def query_by_user_genid(usr_id):
# #     DBSession = sessionmaker(bind=engine)
# #     session=DBSession()
# #     ones=(session.query(OrderObj,RoomObj,HotelObj,OptionObj).filter(

# #         OrderObj.user_genid==usr_id,
# #         OrderObj.valid == 1,
# #         OrderObj.room_genid==RoomObj.genid,
# #         RoomObj.hotel_id==HotelObj.shortName,
# #         OrderObj.status==OptionObj.NoId
# #         ).order_by(OrderObj.modifieddatetime.desc()))
# #     for one in ones:
# #         print(one)
# #     return ones

# # def query_by_admin():
# #     DBSession = sessionmaker(bind=engine)
# #     session=DBSession()
# #     ones=(session.query(OrderObj,RoomObj,HotelObj,OptionObj,UserObj).filter(
# #         OrderObj.user_genid==UserObj.genid,
# #         OrderObj.valid == 1,
# #         OrderObj.room_genid==RoomObj.genid,
# #         RoomObj.hotel_id==HotelObj.shortName,
# #         OrderObj.status==OptionObj.NoId
# #         ).order_by(OrderObj.modifieddatetime.desc()))
# #     for one in ones:
# #         print(one)
# #     return ones
# ###########
