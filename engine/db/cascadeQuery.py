import sys


sys.path.append("..")
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_,and_

##############################
# import CONF as C
# import TOOLS as T
from system import conf as C
from db.dbObjects import LangText,QustObj,User,RFObj,AnswerSheetObj
from db.sysDAO import engine
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

def getQuest_UUID_LANG_RF_ALL(params):  
    
    user_uuid,lang,paperId,*_ = params
    #print( "getQuest_UUID_LANG_RF_ALL" , user_uuid,lang,paperId)
    
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    ones =  session.query( LangText,QustObj,RFObj   ).filter(
        RFObj.cid ==                   user_uuid,
        RFObj.fid == QustObj.paperId,
        QustObj.question_cont == LangText.langcode,
        LangText.language ==             lang,
        QustObj.paperId            ==    paperId
        
    ).order_by(
        QustObj.question_no.asc()
    )
    #print("getQuest_UUID_LANG_RF_ALL" , (ones.count()))
    return ones
#------------------------------------------------------------------------------------#
def getQuest_UUID_LANG_RF_TODO(params):  
    user_uuid,lang,paperId,*_ = params
    #print( "getQuest_UUID_LANG_RF_TODO" , user_uuid,lang,paperId)
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    subQuery= session.query( AnswerSheetObj ).filter(
        AnswerSheetObj.userId == user_uuid,
        AnswerSheetObj.status == "OK"
    )
    # print("getQuest_UUID_LANG_RF_TODO" ,  subQuery.count())
    not_in_list=[]
    for one in subQuery:
        not_in_list.append(one.questId)
        
    
    ones =  session.query( LangText,QustObj,RFObj    ).filter(
        RFObj.cid ==                   user_uuid,
        RFObj.fid == QustObj.paperId,
        QustObj.question_cont == LangText.langcode,
        LangText.language ==             lang,
        QustObj.paperId            ==    paperId,
        
        QustObj.uuid.notin_(   not_in_list    )

    ).order_by(
        QustObj.question_no.asc()
    )
    
    # for one in ones:
    #     print( one[1].uuid )
    #print("getQuest_UUID_LANG_RF_TODO" ,subQuery[0].questId, (ones.count()))
    return ones
#------------------------------------------------------------------------------------#
def get_QA_by_Paper_User(params):
    paperId,userId,LANG,*_ = params
    #print("getAll_Question_byPaperId" , paperId,userId,LANG,"<<")
    DBSession = sessionmaker(bind=engine)
    session=DBSession()
    ones=(session.query(AnswerSheetObj,QustObj,LangText,User).filter(
        AnswerSheetObj.questId == QustObj.uuid,
        QustObj.paperId == paperId,
        QustObj.question_cont == LangText.langcode,
        LangText.language == LANG,
        AnswerSheetObj.userId == User.uuid,
        or_( and_(AnswerSheetObj.userId==userId , AnswerSheetObj.attr=="NORMAL") 
            , (AnswerSheetObj.attr=="COMMENT")),
        QustObj.ifvalid == "YES"  )).order_by(
        QustObj.question_no.asc(), AnswerSheetObj.cDate.asc()
           
        )
    
    print("getAll_Question_byPaperId " ,ones.count())
    return ones
#------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------#
#  def getAnswerSheet_UUID_QUESTID(params):
     
