Data={
  "NLP": {
    "Domain_Name": "Natural Language Processing",
    "Description": "A branch of artificial intelligence that enables computers to understand, interpret, and manipulate human language. It bridges the gap between human communication and computer understanding by processing text and spoken words.",
    "Real_World_App": "1. Customer service chatbots that automatically resolve user inquiries. 2. Sentiment analysis tools used by brands to monitor social media feedback.",
    "Python_Libraries": "NLTK, SpaCy, Hugging Face Transformers"
  },
  "Computer_Vision": {
    "Domain_Name": "Computer Vision",
    "Description": "A field of AI that trains computers to interpret and understand the visual world. It uses digital images from cameras and videos to accurately identify, track, and classify visual objects.",
    "Real_World_App": "1. Facial recognition systems used for smartphone biometric unlocking. 2. Automated defect detection in manufacturing assembly lines.",
    "Python_Libraries": "OpenCV, PyTorch, Albumentations"
  },
  "Speech_Processing": {
    "Domain_Name": "Speech Processing",
    "Description": "The study of speech signals and the processing methods of voice data. It focuses on converting acoustic signals into digital text and generating natural human speech from written digital input.",
    "Real_World_App": "1. Voice assistants like Apple Siri and Amazon Alexa. 2. Real-time automated captioning for live television broadcasts and video meetings.",
    "Python_Libraries": "Librosa, SpeechRecognition, TTS"
  },
  "Robotics": {
    "Domain_Name": "Robotics and Control",
    "Description": "An interdisciplinary domain that combines AI and mechanical engineering to build programmable machines. It focuses on enabling physical systems to perceive their surroundings and execute precise movements.",
    "Real_World_App": "1. Autonomous drones used for agricultural crop monitoring. 2. Robotic arms performing high-precision surgical procedures in hospitals.",
    "Python_Libraries": "ROS (rospy), PyBullet, Pinocchio"
  }
}

bool=True

while bool:
    try: 
        print("\n")
        print("Information are available in to following domain.".center(120," "))
        print("1. NLP\t2. Computer Vision\t3. Speech Processing\t4. Robotics\t5. Exit".center(110," "))
        ch=int(input("\nEnter which domain information you want: "))
        match(ch):
            case 1:
                for d in Data["NLP"].items():
                    print(f"{d[0]} : {d[1]}")
            case 2:
                for d in Data["Computer_Vision"].items():
                    print(f"{d[0]} : {d[1]}")
            case 3:
                for d in Data["Speech_Processing"].items():
                    print(f"{d[0]} : {d[1]}")
            case 4:
                for d in Data["Robotics"].items():
                    print(f"{d[0]} : {d[1]}")
            case 5:
                bool = False
            case default:
                print("Invalid Input! Try again")
    except:
        print("Invalid Input! Try again")
