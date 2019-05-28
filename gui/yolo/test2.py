a=[]
a.append([1,2,3,4])
a.append([2,3,4,5])
a.append([3,4,5,6])
i=0
for q,w,e,r in a:
    print(q,w,e,r)

a=[]


print(a)


else :
    if isTracing:
        success, box=tracker.update(frame)
        print('box = ',box)
        l,t,w,h=box
        l=int(l)
        t=int(t)
        w=int(w)
        h=int(h)
        isStart=True

        tracing_image = frame[t:t+h, l:l+w]
        cv2.imwrite('1.jpg',tracing_image)
        # print(tracing_image)
        # a=tracing_image
        # cv2.imshow("face", tracing_image)
        cv2.rectangle(frame, pt1=(int(l),int(t)), pt2=(int(l)+int(w), int(t)+int(h)) , color=(255,255,255), thickness=3)


    for (top,right,bottom,left) in unKnown_box:
        face_image = frame[top:bottom, left:right]

        # Blur the face image
        face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
        # face_image = cv2.medianBlur(face_image,9)
        # Put the blurred face region back into the frame image
        frame[top:bottom, left:right] = face_image

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        if video_path == 'stream':
            cv2.imshow("face", frame)

    for (top,right,bottom,left) in Known_box:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        if video_path == 'stream':
            cv2.imshow("face", frame)



    if isStart :
        print('l = ',l,' t = ',t, ' w = ',w,' h = ',h)
        # cv2.imshow("face", a)
        t_image = cv2.imread('1.jpg', cv2.IMREAD_COLOR)
        # # tracing_image = cv2.GaussianBlur(tracing_image, (99, 99), 30)
        frame[t:t+h, l:l+w] = t_image
        # cv2.imshow("face", frame[t:t+h, l:l+w])

    if isOutput:
        out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
