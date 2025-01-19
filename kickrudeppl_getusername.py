from PIL import Image
import cv2
import pytesseract
import time
import extractname

def get_rgb_of_pixel(path, x, y):
    img = Image.open(path).convert('RGB')
    r,g,b = img.getpixel((x,y))
    return (r,g,b)

def main(path):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\nyx\Downloads\Tesseract-OCR\tesseract.exe'

    config = r"--psm 6 --oem 3"
    
    extractname.extractText(path)
    img = cv2.imread(path)
    h, w, _ = img.shape
    
    data = pytesseract.image_to_data(img, config=config, output_type=pytesseract.Output.DICT)

    amount_boxes = len(data['text'])
    for i in range(amount_boxes):
        if i == amount_boxes -1:
            (x, y, w, h) = (data['left'][i]-5, data['top'][i]-5, data['width'][i]+5, data['height'][i]+5)
            
            filename = f"testing_{time.time()}.png"
            cropped_img = img[y:(y+h)+2, x:(x+w)+2]

            try:
                cv2.imwrite(filename, cropped_img)    
                img = cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
                img = cv2.putText(img, data['text'][i], (x, y-5), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1, cv2.LINE_AA)
            except:
                pass
    try:
        if len(data['text'][-2]) > len(data['text'][-1]):
            return f"{data['text'][-2]}{data['text'][-1]}"
        return data['text'][-1]
    except:
        return "xx"