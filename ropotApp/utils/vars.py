
class Vars(object):
    def __init__(self):
        # -----  website ---- #
        # websit destination
        self.target_login = "https://extranet.vodafone.com.eg/dealer/#/login"
        self.target_flex = "https://extranet.vodafone.com.eg/dealer/#/services/flex"

        # login
        self.userInput = "#exampleInputEmail1"
        self.passInput = "#exampleInputPassword1"
        self.pinInput = "#exampleInputPin1"
        self.loginBtn = "button.login-btn"

        # select line
        self.lines = "a[href='#/services/flex']"
        # login id
        self.idInput = "input.form-control"
        self.nextBtn = "button.next-btn"

        # select area
        self.titleList = "a.title-color"
        self.listOfBranches = "div.region-search-dropdown a"
        self.listOfAreas = "div.list-group a"
        

        # select numbers
        self.numbers = "tbody tr td.tableTxt"
        self.backbtn = "button.delete-btn"
        self.nextbtn = "button.next-btn"

        self.selectNumber = 'div.custom-radio input'
        self.alert = "div.alert"


"""
<ngx-spinner _ngcontent-pod-c47="" bdopacity="0.6" bdcolor="rgba(51,51,51,0.7)" size="medium" color="#fff" type="ball-clip-rotate" _nghost-pod-c30="" class="ng-tns-c30-0"><!----></ngx-spinner>


<ngx-spinner _ngcontent-pod-c47="" bdopacity="0.6" bdcolor="rgba(51,51,51,0.7)" size="medium" color="#fff" type="ball-clip-rotate" _nghost-pod-c30="" class="ng-tns-c30-0"><!----></ngx-spinner>



<button _ngcontent-pod-c42="" type="button" class="next-btn btn-text enableBtn ml-2 disableNextBtn"><i _ngcontent-pod-c42="" class="fas fa-spin fa-spinner ng-star-inserted"></i><!----> ارسال </button>

01066495536
"""