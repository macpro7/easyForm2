VERSION = "Ver 0.0.3.3"
SECRET_KEY = "EasyForm2"
# DB="sqlite:///../../hdd/db.db" # for p3 sysDAO.py
DB = "sqlite:///../hdd/db.db"  # for main.py
MULTI_LAN_MARK = "Lan3"
MULTI_LAN_SEP = "__"
Request_MARK = ["."]
TEMP_USER_TYPE = "TEMP"
ANCHOR ="_ANCHOR_"
PREFIX="_PREFIX_"
########################################################################################
FILE_PREFIX = "../hdd/conf/"
FILE_MAPPING = {
    "loginpage": "a2f01539b12611e616cefe7139784592",
}

########################################################################################
URLMAPPING = {
    "mainpage": ["Main.htm", "", ""],
    "userTable": ["list.htm", "b_usermanagement", "alert-success"],  # secondary
    "caseTable": ["list.htm", "b_casemgr", "alert-success"],
    "paperTable": ["list.htm", "b_papermgr", "alert-success"],  # warning
    "questTable": ["list.htm", "b_qustmgr", "alert-success"],
    "topicAssTable": ["list.htm", "b_questAssign", "alert-warning"],
    "reviewTable": ["RVLIST.htm", "b_reviewQ", "alert-success"],
}

# -------------------------------------------------------------------------------#
COMBO_FUNC = {
    "getRFView": {
        "name": "getQuestInfoALL",
        "params": ["$User_uuid", "$lang", "$P_OBJID"],
        "method": "getQuestALL",
        "next": "getQuestInfoTodo",
        "result": "count",
        "final": "",
    },
    "getQuestInfoTodo": {
        "name": "getQuestInfoTodo",
        "params": ["$User_uuid", "$lang", "$P_OBJID"],
        "method": "getQuestTodo",
        "result": "",
        "next": "",
        "final": "getQuestFinal",
    },
    # -------------------------#----------------------------#
}

# -------------------------------------------------------------------------------#
CLONE_PROCEDURE = {
    "CloneCaseId": [
        ["uuid", "$g.32"],
        ["tenant_id", ""],
        ["case_name", "APPEND._CLONED"],
        ["case_status", ""],
        ["owner", ""],
    ],
    "CloneUserId": [
        ["uuid", "$g.32"],
        ["login_id", "APPEND._1"],
        ["login_pass", "$g.8"],
        ["displayname", "APPEND._1"],
        ["mobile", ""],
        ["email", ""],
        ["usertype", ""],
        ["validtill", "$AUTODATE.NOW"],
    ],
    "ClonePaperId": [
        ["uuid", "$g.32"],
        ["caseId", ""],
        ["paperNo", ""],
        ["paperNameId", "DEEPCOPY.paperNameId"],
        ["cDate", "$AUTODATE.NOW"],
        ["codeNumber", ""],
        ["paperStatus", "Default.DISABLED"],
        ["ifvalid", ""],
    ],
    "CloneQuestId": [
        ["uuid", "$g.32"],
        ["paperId", ""],
        ["question_no", ""],
        ["question_cont", "DEEPCOPY.question_cont"],
        ["answer_type", ""],
        ["option_id", ""],
        ["attributes", ""],
        ["iftemplate", ""],
        ["ifvalid", ""],
        ["created_datetime", "$AUTODT.NOW"],
        ["created_by", ""],
    ],
}

# -------------------------------------------------------------------------------#

RF_CONF = {
    ############################
    "QuestMain": {
        "pageType": "listPage",
        "getList": "getRF",
        "params": ["$User_uuid", "PAPER_USER"],
        "title": "l_listPaper",
        "colWidth": [30, 30, 20, 20],
        "coltitle": ["l_name", "l_username", "l_status", "l_operation"],
        "colCont": [
            "fid.getPaper_UUID.*paperNameId",
            "cid.getUser_UUID.displayname",
            "status",
            "fid",
        ],
        "chkPage": ["CKQUEST/", "questChkId", "b_check"],
        "rvPage": ["RVQUEST/", "rvQuestId", "b_review"],
        "return": ["Tologin/", "", "b_back"],
    },
    "questChkId": {
        "pageType": "ViewStepByStep",
        "getList": "",
        "getView": "getRFView",
        "title": "l_listPaper",
        "nxtPage": ["CKQUEST/", "questChkId", "b_next"],
        "return": ["Quest/", "QuestMain", "b_back"],
        "data": [  # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "value": "$g.32",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "userId",
                "value": "$User_uuid",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "questId",
                "value": "$getFromPage.QuestId",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "OBJID",
                "value": "$getFromPage.OBJID",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "answerCont",
                "value": "",
                "pageStyle": "INPUT",
            },
            {
                "name": "answerCont_exp",
                "value": "",
                "pageStyle": "INPUT",
            },
            {
                "name": "cDate",
                "value": "$AUTODT.NOW", 
                "pageStyle": "HIDDEN",
            },
            {
                "name": "created_by",
                "value": "$User_uuid",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "attr",
                "value": "NORMAL",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "ans_type",
                "value": "$getFromPage.currentQuestAnswerType",  # LangText,QustObj,RFObj
                "pageStyle": "HIDDEN",
            },
            {
                "name": "status",
                "pageStyle": "HIDDEN",
                "value": "OK",
            },
        ],


    },
    
    ############################
    ########################################
    "": {
        "return": ["", "", "b_back"],
 
    },
    "mainpage": {
        "return": ["", "", "b_back"],
 
    },
    "caseTable": {
        "return": ["work/", "mainpage", "b_back"],
        "operationPage": {           # OPERATION_PAGE
            "Viewb":["CKOBJ/","ViewCaseId","b_check","form_001"],
            "Editb":["EDOBJ/","EditCaseId","b_edit","form_002"],
            "Cloneb":["CLOBJ/","CloneCaseId","b_clone","form_003"],
        },
        "newPage"   : [ "newSimple/", "newCaseId" ,  "b_new" ], 
        "getList"   : "getAll_CaseObj",
        "params"    : ["$User_uuid"],
        "title": "l_listCase",
        "colWidth": [30, 20, 20, 30],
        "coltitle": ["l_name", "l_status", "l_owner", "l_operation"],
        "colCont": [
            "case_name",
            "case_status",
            "owner.GET_USER.displayname",# fid.getPaper_UUID.*paperNameId #QueryValue_colCont
            "uuid",#OBJID
            
            ],
        

    },
    "userTable": {
        "return": ["work/", "mainpage", "b_back"],
        "operationPage": {          # OPERATION_PAGE
            "Viewb":["CKOBJ/","ViewUserId","b_check","form_001"],
            "Editb":["EDOBJ/","EditUserId","b_edit","form_002"],
            "Cloneb":["CLOBJ/","CloneUserId","b_clone","form_003"],
        },
        "newPage"   : [ "newSimple/", "newUserId" ,  "b_new" ], 
        "getList": "getAll_User",
        "params": ["$User_uuid"],

        "title": "l_listUser",
        "colWidth": [20, 20, 20, 20, 20],
        "coltitle": ["l_id", "l_name", "l_type", "l_validPeriod", "l_operation"],
        "colCont": [
            "login_id",#"fid.getPaper_UUID.*paperNameId",
            "displayname",#"cid.getUser_UUID.displayname",
            "usertype",#"status",
            "validtill",#"fid",
            "uuid",
        ],
        
        

    },
    "paperTable": {
        "return": ["work/", "mainpage", "b_back"],
        "operationPage": {           # OPERATION_PAGE
            "Viewb":["CKOBJ/","ViewPaperId","b_check","form_001"],
            "Editb":["EDOBJ/","EditPaperId","b_edit","form_002"],
            "Cloneb":["CLOBJ/","ClonePaperId","b_clone","form_003"],
        },

        "newPage"   : [ "newSimple/", "newPaperId" ,  "b_new" ], 
        "getList" : "getAll_Paper_Valid",
        "params": ["$User_uuid"],
        "title": "l_listPaper",
        "colWidth": [20, 10, 20, 10, 10, 20],
        "coltitle": ["l_uppername", "l_no", "l_name", "l_cdate", "l_status", "l_operation"],
        "colCont": [
            "caseId.getCasebyUUID.case_name",
            "paperNo",
            "*paperNameId",
            "cDate",
            "paperStatus",
            "uuid",
        ],
        
 
    },
    "questTable": {
        "return": ["work/", "mainpage", "b_back"],
        "operationPage": {           # OPERATION_PAGE
            "Viewb":["CKOBJ/","ViewQuestId","b_check","form_001"],
            "Editb":["EDOBJ/","EditQuestId","b_edit","form_002"],
            "Cloneb":["CLOBJ/","CloneQuestId","b_clone","form_003"],
        },

        "newPage"   : [ "newSimple/", "newQuestId" ,  "b_new" ], 
        "getList" : "getAll_Question_Valid",
        "params": ["$User_uuid"],
        "title": "l_listQuest",
        "colWidth": [20, 10, 20, 10, 10, 20],
        "coltitle": ["l_uppername", "l_no", "l_name", "l_cdate", "l_status", "l_operation"],
        "colCont": [
            "paperId.getPaper_UUID.*paperNameId",
            "question_no",
            "*question_cont",
            "created_datetime",
            "ifvalid",
            "uuid",
        ],

    },
    "topicAssTable": {
        "return": ["work/", "mainpage", "b_back"],
        "operationPage": {           # OPERATION_PAGE
            "Viewb":["CKOBJ/","ViewTopAssId","b_check","form_001"],
            "Editb":["EDOBJ/","EditTopAssId","b_edit","form_002"],
            "Cloneb":["CLOBJ/","CloneTopAssId","b_clone","form_003"],
        },
        
        "newPage"   : [ "newSimple/", "newTopAssId" ,  "b_new" ], 
        

    },
    "reviewTable": {
        "return": ["work/", "mainpage", "b_back"],
        "operationPage": {           # OPERATION_PAGE
            "Viewb":["RVQ/","ReviewPaperbyUser","l_user","form_001"],
            # "Editb":["EDOBJ/","EditPaperId","b_edit","form_002"],
            # "Cloneb":["CLOBJ/","ClonePaperId","b_clone","form_003"],
        },

        #"newPage"   : [ "newSimple/", "newPaperId" ,  "b_new" ], 
        "getList" : "getAll_Paper_Valid",
        "params": ["$User_uuid"],
        "title": "l_listPaper",
        "colWidth": [15, 10, 25, 15, 15, 20],
        "coltitle": ["l_uppername", "l_no", "l_name", "l_UserAssigned", "l_UserFinished", "b_check"],
        "colCont": [
            "caseId.getCasebyUUID.case_name",
            "paperNo",
            "*paperNameId",
            "uuid.getAssigned_FID.COUNT",
            "uuid.getFinishedUser.LEN",
            "uuid.getFinishedUser.OBJ",
            "uuid",
        ],
        
 
    },
    "ReviewPaperbyUser": {
        "return": ["work/", "reviewTable", "b_back"],
        "operationPage": {           # OPERATION_PAGE
            "Viewb":["RVQ/","ReviewPaperUser","ViewUserId","form_001"],
            # "Editb":["EDOBJ/","EditPaperId","b_edit","form_002"],
            # "Cloneb":["CLOBJ/","ClonePaperId","b_clone","form_003"],
        },

        #"newPage"   : [ "newSimple/", "newPaperId" ,  "b_new" ], 
        "getList" : "get_QA_by_Paper_User",
        "pageType": "GroupViewPage",
        "params": ["$FOBJID","$COBJID","$lang"],
        "title": "ViewPaperId",
        "data": [ # BuildListPage # AnswerSheetObj,QustObj,LangText,User
            {
                "name": "qu.number",
                "show" : "l_no",
                "cont": "1.question_no",
                "pageCode": "<h6 class='card-title'>_PREFIX__ANCHOR_</h6>",
                "pageStyle": "TEXT",
            },
            
            {
                "name": "q.name",
                "show" : "l_question",
                "cont": "2.text",
                "pageCode":"<p class='card-text'>_PREFIX__ANCHOR_</p>",
                "class": "card-text",
                "pageStyle": "TEXT",
            },
            {
                "name": "username",
                "show" : "l_user",
                "cont": "3.displayname",
                #"pageCode":"<h6 class='card-subtitle mb-2 text-muted'>_PREFIX_  _ANCHOR_</h6>",
                "pageCode":"<p class='card-text'><small class='text-muted'>_PREFIX_  _ANCHOR_</small></p>",
                "class": "card-subtitle mb-2 text-muted",
                "pageStyle": "TEXT",
                "ROLE" :"LIST",
            },
            {
                "name": "a.cont",
                "show" : "l_answer",
                "cont": "0.answerCont",
                "pageCode":"<p class='card-text'><small class='text-muted'>_PREFIX_  _ANCHOR_</small></p><p>&nbsp;</p>",
                #"pageCode":"<h6 class='card-subtitle mb-2 text-muted'>_PREFIX_  _ANCHOR_</h6>",
                "class": "card-text",
                "pageStyle": "TEXT",
                "ROLE" :"LIST",
            },
            {
                "name": "qid_html",
                "show" : "l_answer",
                "cont": "0.questId",
                "pageCode":"<input id='id' name='name'  type='hidden' vaule='_ANCHOR_' />",
                "class": "card-text",
                "pageStyle": "HIDDEN",
                "ROLE" :"HTML",
                
            },
            # {
            #     "name": "qid_link",
            #     "show" : "l_answer",
            #     "cont": "0.uuid",
            #     "pageCode":"    ",
            #     "class": "card-text",
            #     "pageStyle": "LINK",
            #     "ROLE" :"KEY",
                
            # },
            {
                "name": "qid_html",
                "show" : "l_answer",
                "cont": "0.questId",
                "pageCode":"<input id='qid' name='qid'  type='hidden' vaule='_ANCHOR_' />",
                "class": "card-text",
                "pageStyle": "HIDDEN",
                "ROLE" :"KEY",
                
            },
            
            
        ],
        # "colWidth": [15, 35, 20, 30],
        # "coltitle": ["l_no", "l_name",  "l_UserFinished", "l_listUser"],
        # "colCont": [
        #     #"caseId.getCasebyUUID.case_name",
        #     "paperNo",
        #     "paperNameId",
        #     "uuid.getFinishedUser.LEN",
        #     "uuid.getFinishedUser.OBJ",
        # ],
        
 
    },
    "ReviewPavvvvvvvvvperUser": {
        "return": ["RVQ/", "ReviewPaperList", "b_back"],
        "operationPage": {           # OPERATION_PAGE
            "Viewb":["RVQ/","ReviewPaperUser","b_check","form_001"],
            # "Editb":["EDOBJ/","EditPaperId","b_edit","form_002"],
            # "Cloneb":["CLOBJ/","ClonePaperId","b_clone","form_003"],
        },

        #"newPage"   : [ "newSimple/", "newPaperId" ,  "b_new" ], 
        "getList" : "getAll_Paper_Valid",
        "params": ["$User_uuid"],
        "title": "l_listPaper",
        "colWidth": [15, 35, 20, 30],
        "coltitle": ["l_no", "l_name",  "l_UserFinished", "l_listUser"],
        "colCont": [
            #"caseId.getCasebyUUID.case_name",
            "paperNo",
            "*paperNameId",
            "uuid.getFinishedUser.LEN",
            "uuid.getFinishedUser.OBJ",
        ],
        
 
    },
    ####################
    "ViewTopAssId": {
        "return": ["work/", "topicAssTable", "b_back"],

    },
    "newTopAssId": {
        "nextPageId": "topicAssTable",
        "return": ["work/", "topicAssTable", "b_back"],
        "newPage"   : [ "subNewSimple/", "newTopAssId" ,  "b_new" ], 
 
    },
    "EditTopAssId": {
        "nextPageId": "topicAssTable",
        "return": ["work/", "topicAssTable", "b_back"],
 
        "newPage"   : [ "subEditSimple/", "EditTopAssId" ,  "b_submit" ], 

    },
    "CloneTopAssId": {
        "nextPageId": "topicAssTable",
    },
    ########################
    "ViewCaseId": {
        "return": ["work/", "caseTable", "b_back"],
        "pageType": "ViewPage",
        "title" : "ViewCaseId", 
        "getView": "getCasebyUUID", 
        "data": [ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "value": "uuid",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "tenant_id",
                "value": "tenant_id",
                "show": "TenantId",
                "pageStyle": "TEXT",
            },
            
            {
                "name": "case_name",
                "value": "",
                "show": "Case_Name",
                "pageStyle": "TEXT",

            },
            {
                "name": "case_status",
                "value": "",
                "show": "Case_status",
                "attr":"",
                "pageStyle": "SSELECT",
                "sub":"MISC.CASE_STATUS",

            },
            {
                "name": "owner",
                "value": "$GET_UNAME",
                "show": "Owner",
                "pageStyle": "TEXT",

               
            },
        ],
 
    },
    "newCaseId": {
        "pageType": "NewPage",
        "nextPageId": "caseTable",
        "return": ["work/", "caseTable", "b_back"],
        "title" : "l_addItem", 
        "next"  : [ "subNewSimple/", "newCaseId" ,  "b_new" ], 


        "data": [ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "show": "uuid",
                "attr":"readonly",
                "value": "$g.32",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "tenant_id",
                "value": "$g.32",
                "show": "tenant_id",
                "attr":"readonly",
                "pageStyle": "HIDDEN",
            },
            
            {
                "name": "case_name",
                "value": "",
                "show": "Case_Name",
                "attr":"",
                "pageStyle": "TEXT",
                #"attr":"readonly",
            },
            {
                "name": "case_status",
                "value": "",
                "show": "Case_status",
                "attr":"",
                "pageStyle": "SSELECT",
                "sub":"MISC.CASE_STATUS",
            },
            {
                "name": "owner_name",
                "value": "$User_uuid",
                "show": "Owner",
                "pageStyle": "HIDDEN",
                "attr":"readonly",
               
            },
            {
                "name": "owner",
                "value": "$User_uuid",
                "show": "Owner",
                "pageStyle": "HIDDEN",

               
            },

        ],
        
 
    },
    "EditCaseId": {
        "title" : "l_infoEdit", 
        "nextPageId": "caseTable",
        "pageType": "EditPage",
        "return": ["work/", "caseTable", "b_back"],
        "next"   : [ "subEditSimple/", "EditCaseId" ,  "b_submit" ], 
        "getView": "getCasebyUUID", 
        "data": [ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "value": "uuid",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "tenant_id",
                "value": "tenant_id",
                "show": "TenantId",
                "attr":"readonly",
                "pageStyle": "TEXT",
            },
            
            {
                "name": "case_name",
                "value": "",
                "show": "Case_Name",
                "pageStyle": "TEXT",

            },
            {
                "name": "case_status",
                "value": "",
                "show": "Case_status",
                "attr":"",
                "pageStyle": "SSELECT",
                "sub":"MISC.CASE_STATUS",

            },
            {
                "name": "owner",
                "value": "$GET_UNAME",
                "show": "Owner",
                "pageStyle": "TEXT",
                "pageStyle": "SSELECT",
                "sub":"USER.TEMP",

               
            },
        ],
        
 
    },
    "CloneCaseId": {
        "nextPageId": "caseTable",
    },
    ########################
    "newUserId": {
        "pageType": "NewPage",
        "nextPageId": "userTable",
        "return": ["work/", "userTable", "b_back"],
        "next"   : [ "subNewSimple/", "newUserId" ,  "b_new" ], 
        "title" : "l_addItem", 
        "data": # p_SIMPLE_UI() ; method in "value"
            [
            {
                "name": "uuid",
                "show": "uuid",
                "attr":"readonly",
                "value": "$g.32",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "login_id",
                "value": "",
                "show":"Login Id",
                "pageStyle": "TEXT",
            },
            {
                "name": "login_pass",
                "value": "$g.8",
                "show":"Login Pass",
                "pageStyle": "TEXT",
            },
            {
                "name": "displayname",
                "value": "",
                "show":"Name",
                "pageStyle": "TEXT",
            },
            {
                "name": "mobile",
                "value": "",
                "show":"Mobile",
                "pageStyle": "TEXT",
            },
            {
                "name": "email",
                "value": "",
                "show":"Email",
                "pageStyle": "TEXT",
            },
            {
                "name": "usertype",
                "value": "",
                "show":"User Type",
                "pageStyle": "SSELECT",
                "sub":"MISC.USER_TYPE",
            },
            {
                "name": "validtill",
                "value": "",
                "show":"Valid Period",
                "pageStyle": "DATE",
            },
            
        ],
        
 
    },
    "ViewUserId": {
        "return": ["work/", "userTable", "b_back"],
        "pageType": "ViewPage",
        "title" : "ViewUserId", 
        "getView": "getUser_UUID",
        "data": [ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "value": "uuid",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "login_id",
                "value": "",
                "show":"Login Id",
                "pageStyle": "TEXT",
            },
            {
                "name": "login_pass",
                "value": "",
                "show":"Login Pass",
                "pageStyle": "TEXT",
            },
            {
                "name": "displayname",
                "value": "",
                "show":"Name",
                "pageStyle": "TEXT",
            },
            {
                "name": "mobile",
                "value": "",
                "show":"Mobile",
                "pageStyle": "TEXT",
            },
            {
                "name": "email",
                "value": "",
                "show":"Email",
                "pageStyle": "TEXT",
            },
            {
                "name": "usertype",
                "value": "",
                "show":"User Type",
                "pageStyle": "SSELECT",
                "sub":"MISC.USER_TYPE",
            },
            {
                "name": "validtill",
                "value": "",
                "show":"Valid Period",
                "pageStyle": "TEXT",
            },
            
        ],
         
        
        
    },
    "EditUserId": {
        "title"     : "l_infoEdit",
        "nextPageId": "userTable",
        "return": ["work/", "userTable", "b_back"],
        "next"   : [ "subEditSimple/", "EditUserId" ,  "b_submit" ], 
        "getView": "getUser_UUID",
        "data":[ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "show": "uuid",
                "attr":"readonly",
                "value": "$g.32",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "login_id",
                "value": "",
                "show":"Login Id",
                "pageStyle": "TEXT",
            },
            {
                "name": "login_pass",
                "value": "$g.8",
                "show":"Login Pass",
                "pageStyle": "TEXT",
            },
            {
                "name": "displayname",
                "value": "",
                "show":"Name",
                "pageStyle": "TEXT",
            },
            {
                "name": "mobile",
                "value": "",
                "show":"Mobile",
                "pageStyle": "TEXT",
            },
            {
                "name": "email",
                "value": "",
                "show":"Email",
                "pageStyle": "TEXT",
            },
            {
                "name": "usertype",
                "value": "",
                "show":"User Type",
                "pageStyle": "SSELECT",
                "sub":"MISC.USER_TYPE",
            },
            {
                "name": "validtill",
                "value": "",
                "show":"Valid Period",
                "pageStyle": "DATE",
            },
            
            ],
 
    },
    "CloneUserId": {
        "nextPageId": "userTable",
    },
    ########################
    "newPaperId": {
        "nextPageId": "paperTable",
        "return": ["work/", "paperTable", "b_back"],
        "pageType": "NewPage",
        "title" : "l_addItem", 
        "next"   : [ "subNewSimple/", "newPaperId" ,  "b_new" ], 
        "data":[  # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "value": "$g.32",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "caseId",
                "value": "",
                "show" : "CaseName",
                "pageStyle": "SSELECT",
                "sub": "CASES.NOPARAM",
            },
            {
                "name": "paperNo",
                "value": "",
                "show" : "Paper Number",
                "pageStyle": "TEXT",
            },
            {
                "name": "Lan3",
                "value":"Lan3",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperNameId",
                "value": "$TEXTGEN.q",
                "show" : "Paper Name Id",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperNameId__EN",
                "value": "EnglishVersion",
                "show" : "Paper Name EN",
                "pageStyle": "TEXT",
            },
            {
                "name": "paperNameId__CH",
                "value": "ChineseVersion",
                "show" : "Paper Name CH",
                "pageStyle": "TEXT",
            },
            {
                "name": "paperNameId__JP",
                "value": "JapaneseVersion",
                "show" : "Paper Name JP",
                "pageStyle": "TEXT",
            },
            {
                "name": "cDate",
                "value": "$AUTODATE.NOW",
                "show" : "Created date",
                "pageStyle": "TEXT",
                "attr":"readonly",
            },
            {
                "name": "codeNumber",
                "value": "",
                "show" : "Code",
                "pageStyle": "TEXT",
            },
            {
                "name": "paperStatus",
                "value": "",
                "show" : "Status",
                "pageStyle": "SSELECT",
                "sub":"MISC.PAPER_STATUS",
            },
            {
                "name": "ifvalid",
                "value": "",
                "show" : "Valid",
                "pageStyle": "SSELECT",
                "sub":"MISC.PAPER_VALID",
            },
            
            ], 
        
 
    },
    "ViewPaperId": {
        "return": ["work/", "paperTable", "b_back"],
        "pageType": "ViewPage",
        "title" : "ViewPaperId", 
        "getView": "getPaper_UUID",
        "data":[ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "value": "",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "caseId",
                "value": "",
                "show" : "CaseId",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperNo",
                "value": "",
                "show" : "Paper Number",
                "pageStyle": "TEXT",
            },
            {
                "name": "paperNameId",
                "value": "paperNameId",
                "show" : "Paper Name Id",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperNameId",
                "value": "*paperNameId",
                "show" : "Paper Name",
                "pageStyle": "TEXT",
            },
            {
                "name": "cDate",
                "value": "",
                "show" : "Created date",
                "pageStyle": "TEXT",
            },
            {
                "name": "codeNumber",
                "value": "",
                "show" : "Code",
                "pageStyle": "TEXT",
            },
            {
                "name": "paperStatus",
                "value": "",
                "show" : "Status",
                "pageStyle": "SSELECT",
                "sub":"MISC.PAPER_STATUS",
            },
            {
                "name": "ifvalid",
                "value": "",
                "show" : "Valid",
                "pageStyle": "SSELECT",
                "sub":"MISC.PAPER_VALID",
            },
            
            ], 
        
    },
    "EditPaperId": {
        "title" : "l_infoEdit", 
        "nextPageId": "paperTable",
        "pageType": "EditPage",
        "return": ["work/", "paperTable", "b_back"],
        "next"   : [ "subEditSimple/", "EditPaperId" ,  "b_submit" ], 
        "getView": "getPaper_UUID",
        "data":[  # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "value": "",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "caseId",
                "value": "",
                "show" : "CaseName",
                "pageStyle": "SSELECT",
                "sub": "CASES.NOPARAM",
            },
            {
                "name": "paperNo",
                "value": "",
                "show" : "Paper Number",
                "pageStyle": "TEXT",
            },
            {
                "name": "Lan3",
                "value":"Lan3",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperNameId",
                "value": "$TEXTGEN.q",
                "show" : "Paper Name Id",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperNameId__EN",
                "value": "paperNameId",
                "show" : "Paper Name EN",
                "pageStyle": "TEXT",
            },
            {
                "name": "paperNameId__CH",
                "value": "paperNameId",
                "show" : "Paper Name CH",
                "pageStyle": "TEXT",
            },
            {
                "name": "paperNameId__JP",
                "value": "paperNameId",
                "show" : "Paper Name JP",
                "pageStyle": "TEXT",
            },
            {
                "name": "cDate",
                "value": "",
                "show" : "Created date",
                "pageStyle": "TEXT",
                "attr":"readonly",
            },
            {
                "name": "codeNumber",
                "value": "",
                "show" : "Code",
                "pageStyle": "TEXT",
            },
            {
                "name": "paperStatus",
                "value": "",
                "show" : "Status",
                "pageStyle": "SSELECT",
                "sub":"MISC.PAPER_STATUS",
            },
            {
                "name": "ifvalid",
                "value": "",
                "show" : "Valid",
                "pageStyle": "SSELECT",
                "sub":"MISC.PAPER_VALID",
            },
            
            ],
 
    },
    "ClonePaperId": {
        "nextPageId": "paperTable",
    },
    ########################
    "newQuestId": {
        "nextPageId": "questTable",
        "return": ["work/", "questTable", "b_back"],
        "title" : "l_addItem", 
        "next"   : [ "subNewSimple/", "newQuestId" ,  "b_new" ], 
        "data":[ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "show": "uuid",
                "value":"$g.32",
                "attr":"readonly",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperId",
                "show": "PaperName",
                "value": "",
                "pageStyle": "SSELECT",
                "sub":"PAPERS.$lang",
            },
            {
                "name": "question_no",
                "show": "Question Number",
                "value": "",
                "pageStyle": "TEXT",
            },
            {
                "name": "Lan3",
                "show": "Lan3",
                "value": "",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "question_cont",
                "show": "question_cont",
                "value": "$TEXTGEN.q",
                "pageStyle": "HIDDEN",
            },
            
            {
                "name": "question_cont__EN",
                "show": "Question Name EN",
                "value": "EnglishVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "question_cont__CH",
                "show": "Question Name CH",
                "value": "ChineseVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "question_cont__JP",
                "show": "Question Name JP",
                "value": "JapaneseVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "answer_type",
                "show": "Answer Type",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.ANSWER_TYPE",
            },
            {
                "name": "option_id",
                "value":"",
                "show": "Options candidates (For Choice Only)",
                "pageStyle": "OPTIONS",
                "sub" :"OPTION.OPTION_",
            },
            {
                "name": "attributes",
                "value":"",
                "show": "Attributes ",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "iftemplate",
                "show": "As Template  ",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.IF_TEMPLATE",
            },
            {
                "name": "ifvalid",
                "show": "Valid",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.PAPER_VALID",
            },
            {
                "name": "created_datetime",
                "show": "Created",
                "value":"$AUTODT.NOW",
                "attr":"readonly",
                "pageStyle": "TEXT",
 
            },
            {
                "name": "created_by",
                "show": "By",
                "value":"$User_uuid",
                "pageStyle": "HIDDEN",
 
            },
            
            
            ],
 
    },
    "ViewQuestId": {
        "return": ["work/", "questTable", "b_back"],
        "pageType": "ViewPage",
        "title" : "ViewQuestId", 
        "getView": "getQuestByUUID", 
        "data":[ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "show": "uuid",
                "value":"",
                "attr":"",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperId",
                "show": "PaperName",
                "value": "$GET_PAPERNAME",
                "pageStyle": "TEXT",

            },
            {
                "name": "question_no",
                "show": "Question Number",
                "value": "",
                "pageStyle": "TEXT",
            },
            {
                "name": "Lan3",
                "show": "Lan3",
                "value": "",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "question_cont",
                "show": "question_cont",
                "value": "",
                "pageStyle": "HIDDEN",
            },
            
            {
                "name": "question_cont__EN",
                "show": "Question Name EN",
                "value": "EnglishVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "question_cont__CH",
                "show": "Question Name CH",
                "value": "ChineseVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "question_cont__JP",
                "show": "Question Name JP",
                "value": "JapaneseVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "answer_type",
                "show": "Answer Type",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.ANSWER_TYPE",
            },
            {
                "name": "option_id",
                "value":"",
                "show": "Options candidates (For Choice Only)",
                "pageStyle": "OPTIONS",
                "sub" :"OPTION.OPTION_",
            },
            {
                "name": "attributes",
                "value":"",
                "show": "Attributes ",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "iftemplate",
                "show": "As Template  ",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.IF_TEMPLATE",
            },
            {
                "name": "ifvalid",
                "show": "Valid",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.PAPER_VALID",
            },
            {
                "name": "created_datetime",
                "show": "Created",
                "value":"",
                "attr":"readonly",
                "pageStyle": "TEXT",
 
            },
            {
                "name": "created_by",
                "show": "By",
                "value":"$GET_UNAME",
                "pageStyle": "TEXT",
 
            },
            
            
            ],
 
    },
    "EditQuestId": {
        "title" : "l_infoEdit", 
        "nextPageId": "questTable",
        "return": ["work/", "questTable", "b_back"],
        "pageType": "EditPage",
        "next"   : [ "subEditSimple/", "EditQuestId" ,  "b_submit" ], 
        "getView": "getQuestByUUID", 
        "data":[ # p_SIMPLE_UI() ; method in "value"
            {
                "name": "uuid",
                "show": "uuid",
                "value":"",
                "attr":"",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "paperId",
                "show": "PaperName",
                "value": "$GET_PAPERNAME",
                "pageStyle": "SSELECT",
                "sub":"PAPERS.$lang",

            },
            {
                "name": "question_no",
                "show": "Question Number",
                "value": "",
                "pageStyle": "TEXT",
            },
            {
                "name": "Lan3",
                "show": "Lan3",
                "value": "",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "question_cont",
                "show": "question_cont",
                "value": "",
                "pageStyle": "HIDDEN",
            },
            
            {
                "name": "question_cont__EN",
                "show": "Question Name EN",
                "value": "EnglishVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "question_cont__CH",
                "show": "Question Name CH",
                "value": "ChineseVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "question_cont__JP",
                "show": "Question Name JP",
                "value": "JapaneseVersion",
                "pageStyle": "TEXT",
            },
            {
                "name": "answer_type",
                "show": "Answer Type",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.ANSWER_TYPE",
            },
            {
                "name": "option_id",
                "value":"",
                "show": "Options candidates (For Choice Only)",
                "pageStyle": "OPTIONS",
                "sub" :"OPTION.OPTION_",
            },
            {
                "name": "attributes",
                "value":"",
                "show": "Attributes ",
                "pageStyle": "HIDDEN",
            },
            {
                "name": "iftemplate",
                "show": "As Template  ",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.IF_TEMPLATE",
            },
            {
                "name": "ifvalid",
                "show": "Valid",
                "value":"",
                "pageStyle": "SSELECT",
                "sub" :"MISC.PAPER_VALID",
            },
            {
                "name": "created_datetime",
                "show": "Created",
                "value":"",
                "attr":"readonly",
                "pageStyle": "TEXT",
 
            },
            {
                "name": "created_by",
                "show": "By",
                "value":"",
                "pageStyle": "HIDDEN",
 
            },
            {
                "name": "created_by",
                "show": "By",
                "value":"$GET_UNAME",
                "attr":"readonly",
                "pageStyle": "TEXT",
 
            },
            
            
            
            ],

    },
    "CloneQuestId": {
        "nextPageId": "questTable",
    },
    ########################
    ########################
    ########################
}


# -------------------------------------------------------------------------------#


# -------------------------------------------------------------------------------#


########################################################################################


########################################################################################


########################################################################################

########################################################################################

#####################################################################################################################

#####################################################################################################################


#####################################################################################################################
