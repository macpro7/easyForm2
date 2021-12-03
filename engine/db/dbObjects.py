import sys


sys.path.append("..")
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime



##############################
# import CONF as C
# import TOOLS as T
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
class LangText(Base):
    __tablename__ = "t_lang"
    id = Column("uuid", Integer, primary_key=True)
    langcode = Column(String)  # ,primary_key=True)
    language = Column(String)
    text = Column(String)

    def __repr__(self):
        return '{ langcode : "%s",language : "%s",text : "%s"}' % (
            self.langcode,
            self.language,
            self.text,
        )
##---------------------------------------------------##
class AnswerSheetObj(Base):
    __tablename__ = "answersheet_obj"
    id=Column('uid',Integer,primary_key=True)
    uuid = Column(String)
    userId = Column(String)
    questId = Column(String)
    answerCont = Column(String)
    cDate = Column(String)
    created_by = Column(String)
    attr = Column(String)
    ans_type = Column(String)
    status = Column(String)

    def __repr__(self):
        return '{ uuid : "%s",userId : "%s",questId : "%s",answerCont : "%s",cDate : "%s",created_by : "%s",attr : "%s",ans_type : "%s",status : "%s"}' % (self.uuid,self.userId,self.questId,self.answerCont,self.cDate,self.created_by,self.attr,self.ans_type,self.status)
##---------------------------------------------------##
class CaseObj(Base):
    __tablename__ = "case_obj"
    id = Column("uid", Integer, primary_key=True)
    uuid = Column(String)
    tenant_id = Column(String)
    case_name = Column(String)
    case_status = Column(String)
    owner = Column(String)

    def __repr__(self):
        return (
            '{ uuid : "%s",tenant_id : "%s",case_name : "%s",case_status : "%s",owner : "%s"}'
            % (self.uuid, self.tenant_id, self.case_name, self.case_status, self.owner)
        )


##---------------------------------------------------##
class User(Base):
    __tablename__ = "t_users"
    id = Column("uid", Integer, primary_key=True)
    uuid = Column(String)
    login_id = Column(String)
    login_pass = Column(String)
    displayname = Column(String)
    mobile = Column(String)
    email = Column(String)
    usertype = Column(String)
    validtill = Column(String)

    def __repr__(self):

        return self.login_id, self.mobile
##---------------------------------------------------##
class QustObj(Base):
    __tablename__ = "qust_obj"
    id=Column('uid',Integer,primary_key=True)
    uuid = Column(String)
    paperId = Column(String)
    question_no  = Column(String)
    question_cont = Column(String)
    answer_type  = Column(String)
    option_id = Column(String)
    attributes  = Column(String)
    iftemplate  = Column(String)
    ifvalid = Column(String)
    created_datetime = Column(String)
    created_by = Column(String)

    def __repr__(self):
        return '{ uuid : "%s",paperId : "%s",question_no  : "%s",question_cont : "%s",answer_type  : "%s",option_id : "%s",attributes  : "%s",iftemplate  : "%s",ifvalid : "%s",created_datetime : "%s",created_by : "%s"}' % (self.uuid,self.paperId,self.question_no ,self.question_cont,self.answer_type ,self.option_id,self.attributes ,self.iftemplate ,self.ifvalid,self.created_datetime,self.created_by)

##---------------------------------------------------##
class MiscListObj(Base):
    __tablename__ = "t_misclist_obj"
    id = Column("uid", Integer, primary_key=True)
    uuid = Column(String)
    mcata = Column(String)
    mtext = Column(String)
    ifvalid = Column(String)

    def __repr__(self):
        return '{ uuid : "%s",mcata : "%s",mtext : "%s",ifvalid : "%s"}' % (
            self.uuid,
            self.mcata,
            self.mtext,
            self.ifvalid,
        )


##---------------------------------------------------##
class PaperObj(Base):
    __tablename__ = "paper_obj"
    id = Column("uid", Integer, primary_key=True)
    uuid = Column(String)
    caseId = Column(String)
    paperNo = Column(String)
    paperNameId = Column(String)
    cDate = Column(String)
    codeNumber = Column(String)
    paperStatus = Column(String)
    ifvalid = Column(String)

    def __repr__(self):
        return (
            '{ uuid : "%s",caseId : "%s",paperNo : "%s",paperNameId : "%s",cDate : "%s",codeNumber : "%s",paperStatus : "%s",ifvalid : "%s"}'
            % (
                self.uuid,
                self.caseId,
                self.paperNo,
                self.paperNameId,
                self.cDate,
                self.codeNumber,
                self.paperStatus,
                self.ifvalid,
            )
        )


##---------------------------------------------------##
class RFObj(Base):
    __tablename__ = "rf_obj"
    id = Column("uid", Integer, primary_key=True)
    uuid = Column(String)
    fid = Column(String)
    cid = Column(String)
    attribute = Column(String)
    label = Column(String)
    status = Column(String)

    def __repr__(self):
        return (
            '{ uuid : "%s",fid : "%s",cid : "%s",attribute : "%s",label : "%s",status : "%s" }'
            % (self.uuid, self.fid, self.cid, self.attribute, self.label,self.status)
        )


##############################################################################################################
