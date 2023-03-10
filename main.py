from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
import requests


driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
url = "https://babycuatoi.vn/xep-hinh-thong-minh"
driver.maximize_window()
driver.get(url)

while (1):
    #Click view more button
    userN= driver.find_element(by=By.ID, value="viewmore")
    driver.execute_script("arguments[0].click();", userN)
    
    ##Get the state of button
    xpath = '//div[@class="paginate clearfix"]/a'
    view_more_button = driver.find_elements(by=By.XPATH, value=xpath)
    view_more = [x.get_attribute("textContent") for x in view_more_button]
    
    if view_more[:] != ['Đã hết dữ liệu']: #Check whether view more button disable or not
        #Name
        xpath_1 = '//div[@class="tooltip-content"]/p[@class="name"]'
        list_product_name = driver.find_elements(by=By.XPATH, value=xpath_1)
        product_name = [x.get_attribute("textContent").strip() for x in list_product_name]
        #Price And Discount
        xpath_3 = '//div[@class="list-product clearfix content-list-product-cate"]/div/div/div/div[@class="box-price"]'
        list_product_price_discount = driver.find_elements(by=By.XPATH, value=xpath_3)
        product_price_discount = [x.get_attribute("textContent") for x in list_product_price_discount]
        #Describe
        xpath_4 = '//div[@class="tooltip-content"]/p[@class="des"]'
        list_product_describe = driver.find_elements(by=By.XPATH, value=xpath_4)
        product_describe = [x.get_attribute("textContent") for x in list_product_describe]
        #ImageLink
        xpath_5 = '//div[@class="img"]/a/img'
        list_product_image = driver.find_elements(by=By.XPATH, value=xpath_5)
        product_image_link = [x.get_attribute("src") for x in list_product_image]
    else:
        break
        
#Separate product_price_discount into product_price and product_discount
product_price = []
product_discount = []

for i in range(len(product_price_discount)):
    product_price_discount[i] = product_price_discount[i].replace('\n\t\t\t\t\t\t\t\t',', ').strip().split(',')
    product_price.append(product_price_discount[i][0].replace('₫','').replace('.',''))
    if len(product_price_discount[i]) == 1:
        product_price_discount[i].append('0') 
    product_discount.append((product_price_discount[i][1]).replace('%',''))   
    
#Clean up product_describe data
for i in range(len(product_describe)):
    product_describe[i] = product_describe[i].replace('\n\t\t\t\t\t\t\t\t\t','').\
                                                replace('\n\n\t\t\t\t\t\t',', ').\
                                                replace('-','').replace('✪','').\
                                                replace('-','').replace('✔','').strip()
driver.close()

#Tên sản phẩm, Giá bán, Tỷ lệ giảm giá, Thông tin mô tả sản phẩm, link Hình sản phẩm

#product_name
# product_price
# product_discount
# product_describe
#product_image_link

df = pd.DataFrame({'ProductName':product_name, 'ProductPrice (VND)':product_price, 'ProductDiscount (%)':product_discount, 'ProductDescribe':product_describe, 'ProductImageFileName':product_image_link})
df = df.astype({'ProductDiscount (%)':float})
for i in range (len(df['ProductPrice (VND)'])):
    if df.loc[i,'ProductPrice (VND)'] != 'Liên hệ':
        df.loc[i,'ProductPrice (VND)'] =float(df.loc[i,'ProductPrice (VND)'])
for i in range(df.shape[0]):
    df.loc[i,'ProductImageFileName'] = df.loc[i,'ProductImageFileName'].split('/')[-1]    
#df

df.to_csv('Products.csv', encoding = 'utf-8-sig')

for i in range(df.shape[0]):
    filename = df.loc[i,'ProductImageFileName']
    with open("Images/" + filename, "wb") as f:
        img_response = requests.get(product_image_link[i])
        f.write(img_response.content)