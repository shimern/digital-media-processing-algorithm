import Canny as c

kernel_size = 5
operators= ["Sobel", "Prewitt", "Scharr"]
img_path = ["images/img1.jpg","images/img2.jpg","images/img3.jpg"]
deviations = [0.2,1,20]
borders = [[0.04,0.1],[0.1,0.2],[0.02,0.5]]

#Сравнение значений параметров
for img in img_path:
    for deviation in deviations:
        for border in borders:
            print("deviation: "+deviation+ " border: "+border)
            c.Canny_method(kernel_size, deviation, border,img)




#Сравнение операторов
for operator in operators:
    for img in img_path:
        for deviation in deviations:
            for border in borders:
                print("deviation: " + deviation + " border: " + border)
                c.Canny_method(kernel_size, deviation, border, img, operator)
