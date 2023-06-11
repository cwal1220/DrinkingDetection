import os
import cv2
import numpy as np
from time import sleep
import face_recognition

ROOT = "faces/"

class FaceRecogManager():
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        files = os.listdir(ROOT) # 로그인시 검사할 디렉토리
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.png':
                self.known_face_names.append(name)
                pathname = os.path.join(ROOT, filename)
                img = face_recognition.load_image_file(pathname) # 이미지 로드
                face_encoding = face_recognition.face_encodings(img)[0] 
                self.known_face_encodings.append(face_encoding) # 회원 정보 얼굴 이미지를 저장

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def updateKnownFaces(self):
        self.known_face_encodings = []
        self.known_face_names = []
        files = os.listdir(ROOT) # 로그인시 검사할 디렉토리
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.png':
                self.known_face_names.append(name)
                pathname = os.path.join(ROOT, filename)
                img = face_recognition.load_image_file(pathname) # 이미지 로드
                face_encoding = face_recognition.face_encodings(img)[0] 
                self.known_face_encodings.append(face_encoding) # 회원 정보 얼굴 이미지를 저장

    def getLoginFrame(self, frame):
        name = 'Unknown' # 이름 초기화
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # 속도 향상을 위한 크기 조절(1/4)
        rgb_small_frame = small_frame[:, :, ::-1]

        if self.process_this_frame:
            self.face_locations = face_recognition.face_locations(rgb_small_frame) # 얼굴 위치 확인
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
            # 얼굴 위치를 기반으로 encoding

            # 사용자가 한명도 없으면 얼굴 좌표만 return 해줌
            if len(self.known_face_encodings) <= 0:
                for (top, right, bottom, left) in self.face_locations:
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                return name, frame

            self.face_names = []
            for face_encoding in self.face_encodings:
                # 회원가입되어있는 모든 정보랑 비교
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # 그중 가장 높은값을 저장
                if min_value < 0.4:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            if name != 'Unknown':
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name.split('_')[1], (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        return name, frame

    def getRegisterFrame(self, frame):
        name = 'Unknown' # 이름 초기화
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # 속도 향상을 위한 크기 조절(1/4)

        rgb_small_frame = small_frame[:, :, ::-1]

        if self.process_this_frame:
            self.face_locations = face_recognition.face_locations(rgb_small_frame) # 얼굴 위치 확인
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
            # 얼굴 위치를 기반으로 encoding

            # 얼굴이 감지된 경우
            if(len(self.face_locations) > 0):
                name = "Unknown"

            # 사용자가 한명도 없으면 프레임만 return 해줌
            if len(self.known_face_encodings) <= 0:
                return name, frame

            self.face_names = []
            for face_encoding in self.face_encodings:
                # 회원가입되어있는 모든 정보랑 비교
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # 그중 가장 높은값을 저장
                if min_value < 0.4:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame
        return name, frame


def signUpDuplicatecheck(id): # 회원가입 체크 함수
    for (root, directories, files) in os.walk(ROOT): # 이미지가 있는 폴더에서 파일 검사
        for file in files:
            file_path = os.path.join(root, file)
            if "id_" + id in file_path : # 만약에 폴더내 image 파일에 id가 중복되면 True return
                return True
    return False # 중복된게 없으면 False return


def loginPWcheck(id, pw) : # 로그인 체크 함수
    for (root, directories, files) in os.walk(ROOT): # 이미지가 있는 폴더에서 파일검사
        for file in files:
            file_path = os.path.join(root, file)
            if "id_" + id + "_pw_" + pw in file_path : # ip와 pw가 모두 일치하면
                return True # 로그인 성공
    return False


def signUp(frame, id, pw) :
    face_locations = face_recognition.face_locations(frame) # camera가 찍은 frame중 얼굴만 체크
    if(len(face_locations) == 0) : # 만약 얼굴이 감지되지 않았다면
        print("얼굴이 인식되지 않았습니다. 다시 시도해 주세요")
        return False
    else :
        # 회원가입한 유저 얼굴 저장
        imgArray = np.array(frame) 
        cv2.imwrite(ROOT + "id_" + id + "_pw_" + pw + ".png", imgArray)
        return True



def logIn(cap) :
    print("아이디를 입력하세요 : ", end="")
    id = input()

    faceRecog = FaceRecogManager(cap) # 얼굴인식 객체 생성
    LoginCheck = [] # result check 배열

    while True:
        result = faceRecog.get_frame() # 결과 return
        LoginCheck.append(result) # 저장
        if len(LoginCheck) > 10 : # 10개의 frame을 검사했을때
            LoginResult = [word for word in LoginCheck if id in word] # Login check 배열에 정답이 몇개있는지 확인

            if len(LoginResult) > 7 : # 7개 이상이면 2차비밀번호 check
                print("2차 비밀번호를 입력하세요 : ",end="")
                pw = input()
                
                if loginPWcheck(id=id,pw=pw) :
                    print("로그인 성공")
                else :
                    print("로그인 실패! 2차 비밀번호를 확인하세요.")

                break
            else : # 그게 아니면 return
                print("로그인 실패! 등록된 얼굴이 아닙니다.")
                break
    
    cap.release()


if __name__ == "__main__":
    while True :
        cap = cv2.VideoCapture(0)
        print("1 : 회원가입")
        print("2 : 로그인")

        menu = input()

        if menu == '1' :
            signUp(cap)
        elif menu == '2' :
            logIn(cap)
        else :
            print("잘못된 메뉴입니다.")


        #os.system('cls') # window 환경에서 사용
        #os.system('clear') # linux, mac 환경에서 사용
        
