from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import Student, Teacher, Subject, CourseReg, Quiz, QuizResult
import random
import json
from datetime import datetime


# homepage.
# dynamic things = login thakle nam and relevant link show korbe. Login na thakle login/register show korbe
def home(request):
    if(request.session.has_key('uid')):
        uid = request.session['uid']
        userType = request.session['userType']
        if(userType == 'student'):
            user = Student.objects.get(studentid=uid)
        else:
            user = Teacher.objects.get(teacherid=uid)

        context = {'uid': uid, 'fullname': user.fullname, 'userType': userType}

        return render(request, 'home/index.html', context)

    else:
        return render(request, 'home/index.html')


# for showing student reg page
def stdRegister(request):
    if(request.session.has_key('uid')):  # login obosthay registration show na kore direct dashboard
        return redirect('/dashboard')
    else:
        return render(request, 'studentRegister/index.html')


# for showing teacher reg page
def tcRegister(request):
    if(request.session.has_key('uid')):  # login obosthay registration show na kore direct dashboard
        return redirect('/dashboard')
    else:
        return render(request, 'teacherRegister/index.html')


# For registering students and validation
# student reg form theke data receive kore database e save korbe ei function
def stdRegPost(request):
    studentid = request.POST["studentid"]
    fullname = request.POST["fullname"]
    semester = request.POST["semester"]
    section = request.POST["section"]
    email = request.POST["email"]
    password = request.POST["password"]

    # same id diye duibar reg kortese kina check
    try:
        check_student = Student.objects.get(studentid=studentid)
    except Student.DoesNotExist:
        check_student = None

    if(check_student == None):  # jodi age reg kore na thake tahole database e save hobe std details
        student = Student(studentid=studentid, fullname=fullname, email=email,
                          password=password, semester=semester, section=section)

        student.save()  # saves data in DB

        # reg success dekhabe and then login korte bolbe
        return render(request, 'login/index.html', {'success': "<p class=\"p-3\">Registration Successful!<br>You can now login here.</p>"})

    else:  # jodi same id diye abar reg korte jay tahole ei error show korbe
        return render(request, 'studentRegister/index.html', {'error': "<p class=\"p-3\">ERROR!<br>Student ID " + studentid + " already exists in DB</p>"})


# For registering teachers and validation
# same kaj student reg er moto
def tcRegPost(request):
    teacherid = request.POST['teacherid']
    fullname = request.POST['fullname']
    rank = request.POST['rank']
    email = request.POST['email']
    password = request.POST['password']

    try:
        check_teacher = Teacher.objects.get(teacherid=teacherid)
    except Teacher.DoesNotExist:
        check_teacher = None

    if(check_teacher == None):
        teacher = Teacher(teacherid=teacherid, fullname=fullname,
                          designation=rank, email=email, password=password)
        teacher.save()

        return render(request, 'login/index.html', {'success': "<p class=\"p-3\">Registration Successful!<br>You can now login here.</p>"})

    else:
        return render(request, 'teacherRegister/index.html', {'error': "<p class=\"p-3\">ERROR!<br>Teacher ID " + teacherid + " already exists in DB</p>"})


# for showing login page
def login(request):
    if(request.session.has_key('uid')):  # if user has logged in before, redirecting directly to dashboard
        return redirect('/dashboard')
    else:
        return render(request, 'login/index.html')


# for handling all logins and validation
def loginPost(request):
    uid = request.POST['id']
    password = request.POST['password']
    userType = request.POST['actype']

    # if user is student
    if(userType == 'student'):
        try:
            # student id ta db te ase kina check
            check_student = Student.objects.get(studentid=uid)
        except Student.DoesNotExist:
            check_student = None

        if(check_student != None):  # jodi student id db te pawa jay tahole login korte parbe
            if(check_student.password == password):  # password match kortese kina check

                # jodi pass match kore tahole ekta session create hobe. Jate barbar login na kora lage logout na kora porjnto
                request.session['uid'] = uid
                request.session['userType'] = userType

                # student er subject reg complete thakle dashboard e nibe nahole subject reg korte profile e nibe
                if(check_student.subjects):
                    return redirect('/dashboard')
                else:
                    return redirect('/profile')

            else:  # password wrong hole ei error show korbe
                return render(request, 'login/index.html', {'error': "<p class=\"p-3\">Please try again!<br>You've entered Wrong credentials.</p>"})

        else:  # student id database e na thakleo error show korbe
            return render(request, 'login/index.html', {'error': "<p class=\"p-3\">Please try again!<br>You've entered Wrong credentials.</p>"})

    # -------------------------------------------------------------------------------------

    # if user is teacher
    # student login er moto same kaaj
    else:
        try:
            check_teacher = Teacher.objects.get(teacherid=uid)
        except Teacher.DoesNotExist:
            check_teacher = None

        if(check_teacher != None):
            if(check_teacher.password == password):
                # creating a session for keeping user as logged in until logout
                request.session['uid'] = uid
                request.session['userType'] = userType

                return redirect('/dashboard')
            else:
                return render(request, 'login/index.html', {'error': "<p class=\"p-3\">Please try again!<br>You've entered Wrong credentials.</p>"})

        else:
            return render(request, 'login/index.html', {'error': "<p class=\"p-3\">Please try again!<br>You've entered Wrong credentials.</p>"})


# for showing profile page
def profile(request):
    if(request.session.has_key('uid')):  # user login ase kina check. login thakle only profile e nibe
        uid = request.session['uid']
        userType = request.session['userType']

        if(userType == 'student'):
            # database theke student er details read kortese
            user = Student.objects.get(studentid=uid)
            userDetails = {
                'id': user.studentid,
                'fullname': user.fullname,
                'email': user.email,
                'semester': user.semester,
                'section': user.section,
                'subjects': user.subjects
            }  # student er details

            # course reg request age submit korse kina db theke check
            try:
                # jodi courseReg table e student er req pawa jay tahole details gula db theke niye nibe
                isReg = CourseReg.objects.get(studentid=uid)

            except CourseReg.DoesNotExist:
                isReg = None

            if(isReg == None):  # jodi age corse reg na kore thake
                try:
                    # student er semester onujayi db theke subject read korbe
                    get_sub = Subject.objects.get(semester=user.semester)
                except Subject.DoesNotExist:
                    get_sub = None

                if(get_sub != None):  # subject read kore subject paile subject er ekta array banabe
                    subjects_list = get_sub.subjects.split(',')
                else:
                    subjects_list = None

                # ei data gula html e show korar jonno pass kortese
                context = {
                    'userDetails': userDetails,
                    'userType': userType,
                    'subjects_list': subjects_list
                }

            else:
                context = {
                    'userDetails': userDetails,
                    'userType': userType,
                    'isReg': True  # age reg korse so reg korar option jate na ashe ar
                }

        # -----------------------------------------------------------------------------------------

        # when user is teacher
        else:
            # teacher er data gula db theke read
            user = Teacher.objects.get(teacherid=uid)
            userDetails = {
                'id': user.teacherid,
                'fullname': user.fullname,
                'rank': user.designation,
                'email': user.email,
                'semesters': user.semesters,
                'sections': user.sections,
                'subjects': user.subjects
            }

            # html e pass
            context = {
                'userDetails': userDetails,
                'userType': userType,
            }

        # profile er html page ta render korbe dynamic data diye
        return render(request, 'profile/index.html', context)

    else:
        return redirect('/login')


# dashboard code here...
def dashboard(request):
    if(request.session.has_key('uid')):
        current_datetime = datetime.now()
        uid = request.session['uid']
        userType = request.session['userType']

        if(userType == 'student'):
            user = Student.objects.get(studentid=uid)

            userDetails = {
                'id': user.studentid,
                'fullname': user.fullname
            }

            # student age j quiz gula attend korse tar details read db theke
            attendedQuizs = QuizResult.objects.filter(studentid=uid)

            # exract all attended quiz id
            attendedQuizIds = []
            for attendedQuiz in attendedQuizs:
                attendedQuizIds.append(attendedQuiz.quizid)

            # new kono wuiz attend korar jonno ase kina db te check
            quizs = Quiz.objects.filter(semester=user.semester)

            ableToAttend = []
            # jodi attend korar moto quiz thake
            if(quizs):
                for quiz in quizs:
                    # quiz ta kon kon sec er jonno sheta ekta array te rakhtese
                    sections = quiz.sections.split(', ')
                    if user.section in sections:  # jodi student er section quiz er sathe match kore
                        # student j subjects er jonno reg korse shegular ekta array
                        subjects = user.subjects.split(', ')

                        if quiz.subject in subjects:  # jodi quiz er subject er sathe student er reg kora subject match kore tahole quiz attend korar option ashbe
                            # attend korar moto quiz ta ekta list er rakhbe
                            ableToAttend.append(quiz)

                        else:
                            ableToAttend.append(None)
                    else:
                        ableToAttend.append(None)

                # checking if at least one quiz is available for attending
                test = None
                for ability in ableToAttend:
                    if(ability != None):
                        test = True
                        break

                # html e show korar jonno object jokhon student is eligible to attend
                context = {
                    'userDetails': userDetails,
                    'userType': userType,
                    'quizDetails': ableToAttend,
                    'test': test,
                    'current_datetime': current_datetime,
                    'attendedQuizs': attendedQuizs,
                    'attendedQuizIds': attendedQuizIds
                }

            # jodi kono quiz na thake db te
            else:
                context = {
                    'userDetails': userDetails,
                    'userType': userType
                }

        # -----------------------------------------------------------------------------

        # if user is teacher
        else:
            user = Teacher.objects.get(teacherid=uid)

            userDetails = {
                'id': user.teacherid,
                'fullname': user.fullname
            }

            # teacher er create kora quiz gula db theke read
            quizDetails = Quiz.objects.filter(teacherid=user.teacherid)

            submissions = []  # quiz er student submissions gula store korbe list e

            for quiz in quizDetails:  # shob quiz er jonnoi submission ashse kina check using loop
                # create kora quiz er moddhe konotar answer kono student submit korse kina check
                sub = QuizResult.objects.filter(
                    quizid=quiz.quizid, teacherid=uid)

                if sub:  # jodi submit kore thake kew
                    subDetails = {
                        'quizid': quiz.quizid,
                        'subject': quiz.subject,
                        'semester': quiz.semester,
                        'endtime': quiz.endtime,
                        'totalqs': quiz.totalqs,
                        # quiz tar jonno koyta submission ashse
                        'totalSub': len(sub)
                    }

                    # submit details gula list e rakhbe
                    submissions.append(subDetails)

            context = {
                'userDetails': userDetails,
                'userType': userType,
                'quizDetails': quizDetails,
                'current_datetime': current_datetime,
                'submissions': submissions  # kono submission na thakle list empty
            }

        return render(request, 'dashboard/index.html', context)

    else:
        # user login na kore dashboard e dhukte gele login korte bolbe age
        return redirect('/login')


# student ra j quiz gular answer submit korse tar details
def subDetails(request):
    uid = request.session['uid']
    userType = request.session['userType']

    if userType == 'teacher':  # only teacher dekhte parbe ei page
        user = Teacher.objects.get(teacherid=uid)
        userDetails = {
            'id': user.teacherid,
            'fullname': user.fullname
        }

        # j quiz er submission dekhbe tar id read korbe
        qid = request.GET['quizid']

        # oi quiz id te koyta submission ashse dn theke read korbe and data niye ashbe
        subDetails = QuizResult.objects.filter(quizid=qid)

        quizDetails = Quiz.objects.get(quizid=qid)  # quiz id tar all details

        allAnswers = []  # shob student er deya answer object akare ei list e thakbe

        answers = []  # single student er ans ei list e

        for sub in subDetails:  # loop chalai shob student er submission check
            ansStr = sub.answers  # ans gular string

            # string k convert kore ekta array banabe ans er
            ansArr = ansStr.split('<->')

            for ans in ansArr:  # prottekta question er ans loop diye check
                if(ans):
                    # prottek ta question er answer gula json object e convert
                    ansJson = json.loads(ans)
                    answers.append(ansJson)  # shob ans gula list e rakhlo

            # student er id ar tar deya answer gula diye ekta object banalo
            temp = {
                'stdid': sub.studentid,
                'answers': answers
            }

            allAnswers.append(temp)  # ei list e shobar ans thakbe id onujayi
            answers = []  # answers list ta abar empty kora holo jate arekjon student er deya answer overlap na hoy

        # shob data html page e pass korar jonno
        context = {
            'userDetails': userDetails,
            'quizOb': quizDetails,
            'submissions': subDetails,
            'allAnswers': allAnswers
        }

        # html e pass kora holo shob data
        return render(request, 'submissions/index.html', context)

    # jodi kono student ei link e ashte jay, page not found show korbe
    else:
        return HttpResponse('<h1>404 Page not found!</h1>')


# let the student attend quiz and submit answers
def attendQuiz(request):
    uid = request.session['uid']
    userType = request.session['userType']

    if(userType == 'student'):
        qid = request.GET['quizid']  # j quiz ta attend korbe tar id
        user = Student.objects.get(studentid=uid)

        userDetails = {
            'id': user.studentid,
            'fullname': user.fullname
        }

        quizOb = Quiz.objects.get(quizid=qid)  # quiz tar details db theke read

        # formatting questins as an object
        questionsStr = quizOb.questions
        qsArray = questionsStr.split('<->')
        qsJSONlist = []

        # for calculating the remaining time | countdown timer banate kaje lagbe
        endtime = quizOb.endtime
        endtime_ms = endtime.timestamp() * 1000

        # question er array theke question gula object e convert kore arekta list e rakha holo
        for qs in qsArray:
            if(qs):
                qsJSON = json.loads(qs)
                qsJSONlist.append(qsJSON)

        context = {
            'userDetails': userDetails,
            'userType': userType,
            'questions': qsJSONlist,
            'quizOb': quizOb,
            'endtime': endtime_ms
        }

        return render(request, 'attendQuiz/index.html', context)

    else:
        return HttpResponse('<h1>404 Page not found!</h1>')


#student quiz er answer submit korar por scroing korar function
def judgement(request):
    if request.method == 'POST':
        uid = request.session['uid']
        std = Student.objects.get(studentid=uid)

        qid = request.POST['quizid']
        studentid = request.POST['studentid']
        stdName = request.POST['std-name']
        teacherid = request.POST['teacherid']
        semester = request.POST['semester']
        subject = request.POST['subject']
        attendtime = datetime.now()
        totalqs = int(request.POST['totalqs'])

        #print(qid, studentid, teacherid, totalqs)
        answers = []
        ansStr = ""

        # receiving ans data as a object
        for i in range(totalqs):
            ans = {
                'qno': i+1,
                'answer': request.POST.get("Q"+str(i+1)+"ANS", False)
            }
            answers.append(ans)

        # formatting answers a json string
        for ans in answers:
            temp_json = json.dumps(ans)
            ansStr = ansStr + "<->" + str(temp_json)

        # scoring the student
        qsJSONlist = []
        score = 0
        count = 0
        quizOb = Quiz.objects.get(quizid=qid)
        questions = quizOb.questions
        qsArray = questions.split('<->')

        # converting questions to json obj to check 'ans' key
        for qs in qsArray:
            if(qs):
                tempJson = json.loads(qs)
                qsJSONlist.append(tempJson)

        # checking all answers with database and scoring up
        for qsJSON in qsJSONlist:
            if answers[count]['qno'] == qsJSON['qno']:
                if qsJSON['ans'] == answers[count]['answer']: #teacher er deya ans er sathe student er deya ans matching
                    score = score + 1
            count = count+1

        #student er submit kora ans and other details db te save
        result = QuizResult(studentid=studentid, stdname=stdName, teacherid=teacherid, quizid=qid, section=std.section,semester=semester, subject=subject, attendtime=attendtime, totalqs=totalqs, answers=ansStr, score=score)
        result.save()

        return redirect('/dashboard')

    else:
        return HttpResponse('<h1>404 Page not found!</h1>')


# for teacher | quiz er questions/ans every details show korbe
def viewQuiz(request):
    userType = request.session['userType']

    # jodi user teacher hoy taholei ei page e jete parbe
    if userType == 'teacher':
        uid = request.session['uid']
        qid = request.GET['quizid']
        user = Teacher.objects.get(teacherid=uid)

        userDetails = {
            'id': user.teacherid,
            'fullname': user.fullname
        }

        # retrieving quiz details
        quizOb = Quiz.objects.get(quizid=qid)

        questionsStr = quizOb.questions

        qsArray = questionsStr.split('<->') #qs gulake array te rakhbe
        qsJSONlist = []

        for qs in qsArray:
            if(qs):
                qsJSON = json.loads(qs) #qs gulake json object e convert
                print(qsJSON) 
                qsJSONlist.append(qsJSON)

        context = {
            'userDetails': userDetails,
            'questions': qsJSONlist,
            'quizOb': quizOb
        }

        return render(request, 'viewQuiz/index.html', context)

    else:
        return HttpResponse('<h1>404 Page not found!</h1>')


# for verifying advisor password
def verify(request):
    if request.method == 'POST':
        password = request.POST['password']
        if(password == 'advisor123'):
            return redirect('/seeCourseReq')
        else:
            return HttpResponse('Sorry password incorrect!')

    else:
        return HttpResponse('<h1>404 Page not found!</h1>')


# for showing all course reg reqs
def seeCourseReq(request):
    userType = request.session['userType']

    if userType == 'teacher':
        uid = request.session['uid']
        user = Teacher.objects.get(teacherid=uid)

        userDetails = {
            'id': user.teacherid,
            'fullname': user.fullname,
        }

        all_requests = CourseReg.objects.all() # db theke reg req gula read kore store kortese ekta object e

        context = {
            'userDetails': userDetails,
            'all_requests': all_requests
        }

        return render(request, 'seeCourseReg/index.html', context)

    else:
        return HttpResponse('<h1>404 Page not found!</h1>')


# hadling course reg
def stdSubjectsPost(request):
    subjects = request.POST.getlist('subjects[]')
    subjects_str = ""
    for subject in subjects:
        subjects_str = subjects_str + subject + ", "

    uid = request.session['uid']

    check_student = Student.objects.get(studentid=uid)

    courseReg = CourseReg(studentid=uid, fullname=check_student.fullname,
                          semester=check_student.semester, section=check_student.section, subjects=subjects_str)
    courseReg.save()

    return redirect('/profile')


# accept course reg
def acceptReg(request):
    uid = request.POST['acceptid']
    subjects = request.POST['subjects']

    get_student = Student.objects.get(studentid=uid)
    get_student.subjects = subjects
    get_student.save()

    obj = CourseReg.objects.get(studentid=uid)
    obj.delete()

    # retrieving teacher
    uid = request.session['uid']
    user = Teacher.objects.get(teacherid=uid)

    userDetails = {
        'id': user.teacherid,
        'fullname': user.fullname,
    }

    all_requests = CourseReg.objects.all()

    context = {
        'userDetails': userDetails,
        'all_requests': all_requests,
        'success': True,
        'acceptid': request.POST['acceptid']
    }

    return render(request, 'seeCourseReg/index.html', context)


# when reject button is pressed
def rejectReg(request):
    uid = request.POST['rejectid']

    obj = CourseReg.objects.get(studentid=uid)  # DB
    obj.delete()

    # retrieving teacher
    uid = request.session['uid']
    user = Teacher.objects.get(teacherid=uid)

    userDetails = {
        'id': user.teacherid,
        'fullname': user.fullname,
    }

    all_requests = CourseReg.objects.all()

    context = {
        'userDetails': userDetails,
        'all_requests': all_requests,
        'reject': True,
        'rejectid': request.POST['rejectid']
    }

    return render(request, 'seeCourseReg/index.html', context)


# for filtering course reg by semester/section
def filterReq(request):
    semester = request.GET['semester']
    section = request.GET['section']
    context = {}

    # retrieving teacher
    uid = request.session['uid']
    user = Teacher.objects.get(teacherid=uid)

    userDetails = {
        'id': user.teacherid,
        'fullname': user.fullname,
    }

    if(semester):
        all_requests = CourseReg.objects.filter(semester=semester)
        context = {
            'userDetails': userDetails,
            'all_requests': all_requests,
        }
    else:
        all_requests = CourseReg.objects.filter(section=section)
        context = {
            'userDetails': userDetails,
            'all_requests': all_requests,
        }

    return render(request, 'seeCourseReg/index.html', context)


# user logout
def logout(request):
    try:
        del request.session['uid']
        del request.session['userType']
        return redirect('/login')
    except:
        return HttpResponse('<h1>Internal server error!</h1>')


# create quiz part for teacher
def createQuiz(request):
    if(request.method == 'GET'):
        quizid = random.randint(1, 50000)
        uid = request.session['uid']
        userType = request.session['userType']
        user = Teacher.objects.get(teacherid=uid)

        userDetails = {
            'id': user.teacherid,
            'fullname': user.fullname,
        }

        context = {
            'userDetails': userDetails,
            'userType': userType,
            'qid': quizid
        }

        return render(request, 'createQuiz/index.html', context)

    if(request.method == 'POST'):
        sectionStr = ""
        qid = request.POST['quizid']
        teacherid = request.POST['teacherid']
        semester = request.POST['semester']
        sections = request.POST.getlist('sections[]')
        totalqs = int(request.POST['totalqs'])
        starttime = request.POST['start-time']
        endtime = request.POST['end-time']

        for section in sections:
            sectionStr = sectionStr + section + ", "

        quiz = Quiz(quizid=qid, teacherid=teacherid, semester=semester, sections=sectionStr,
                    totalqs=totalqs, starttime=starttime, endtime=endtime)
        quiz.save()

        get_sub = Subject.objects.get(semester=semester)
        subjects = get_sub.subjects.split(',')

        uid = request.session['uid']
        userType = request.session['userType']
        user = Teacher.objects.get(teacherid=uid)

        userDetails = {
            'id': user.teacherid,
            'fullname': user.fullname,
        }

        text = ""

        for i in range(totalqs):
            text = text + 'x'
        print(text)

        context = {
            'userDetails': userDetails,
            'userType': userType,
            'subjects': subjects,
            'totalqs': totalqs,
            'quizid': qid,
            'semester': semester,
            'text': text
        }

        return render(request, 'createQuiz/index-next.html', context)


# save teacher's created quiz in db
def postQuiz(request):
    totalqs = int(request.POST['totalqs'])
    qid = request.POST['quizid']
    subject = request.POST['subject']

    # first save the quiz subject
    save_quiz = Quiz.objects.get(quizid=qid)
    save_quiz.subject = subject
    save_quiz.save()

    # formatting questions to json
    questions = []
    qsStr = ""
    for i in range(totalqs):
        question = {
            'qno': i+1,
            'qs': request.POST["Q"+str(i+1)],
            'options': {
                'A': request.POST["Q"+str(i+1)+"OPA"],
                'B': request.POST["Q"+str(i+1)+"OPB"],
                'C': request.POST["Q"+str(i+1)+"OPC"],
                'D': request.POST["Q"+str(i+1)+"OPD"]
            },
            'ans': request.POST["Q"+str(i+1)+"ANS"]
        }
        questions.append(question)

    for question in questions:
        temp_json = json.dumps(question)
        qsStr = qsStr + "<->" + str(temp_json)

    save_quiz.questions = qsStr
    save_quiz.save()

    return redirect('/dashboard')
