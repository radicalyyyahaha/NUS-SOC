from tools import print1, frame_width, frame_height, cap, model, your_face_encoding, app

from ball import start_ball

from face import start_face


def play_ball():
    start_ball(frame_width, frame_height, cap, model)
    start_face(frame_width, frame_height, cap, your_face_encoding, app)


def rotate():
    print1('C')


def hello():
    print1('P')

# while True:
#     user_input = input("Enter 1 to execute playing ball, 2 to execute rotate, 3 to execute hello, or q to quit: ")
#
#     if user_input == '1':
#         play_ball()
#     elif user_input == '2':
#         rotate()
#     elif user_input == '3':
#         hello()
#     elif user_input.lower() == 'q':
#         print("Exiting the program.")
#         break
