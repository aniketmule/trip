import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from .findElementSafe import HelperMethods as HM
from selenium.common.exceptions import NoSuchElementException
import re
import xlsxwriter

class BrowserAction:
    driver = HM.driver

    def create_workbook(self):
        workbook = xlsxwriter.Workbook('Trip.xlsx')
        worksheet = workbook.add_worksheet("Hotelinfo")
        worksheet.write('A1', 'City')
        worksheet.write('B1', 'Check-In Date')
        worksheet.write('C1', 'Check-Out Date')
        worksheet.write('D1', 'Nights')
        worksheet.write('E1', 'Adults')
        worksheet.write('F1', 'Hotel Name')
        worksheet.write('G1', 'Hotel Stars')
        worksheet.write('H1', 'Room Name')
        worksheet.write('I1', 'Beds')
        worksheet.write('J1', 'Amenities')
        worksheet.write('K1', 'Avg. Price Per Room / Night')
        return workbook

    def get_site(self,url):
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        wait = WebDriverWait(self.driver, 10)

    def scroll_until_load_button_displayed(self):
        while True:
            try:
                end_element = self.driver.find_elements_by_class_name("nothing")
            except NoSuchElementException:
                end_element = False

            print("Element "+str(end_element))
            if not end_element:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                break

#        for hotel in hotel_element_list:
#            print("Hotel: " +hotel.text, end="\n")

    def get_hotel_info(self,workbook):

        workbook_row_index = 1
        workbook_column_index = 0

        destination = self.driver.find_element_by_id("hotels-destination").get_attribute("value")
        guestinfo = self.driver.find_element_by_class_name("info.show-hightlight").text
        check_in_date = self.driver.find_element_by_class_name("focus-input.show-hightlight.in-time").get_attribute(
            "data-key")
        check_out_date = self.driver.find_element_by_class_name("focus-input.show-hightlight.out-time").get_attribute(
            "data-key")
        nights = self.driver.find_element_by_class_name("nights").text

        hotel_element_list = self.driver.find_elements_by_class_name("name.font-bold")
        print("HE LIST: "+str(hotel_element_list))
        self.driver.find_element_by_tag_name('body').send_keys(Keys.HOME)

        for hotel in hotel_element_list:
            self.driver.switch_to.window(self.driver.window_handles[0])

            time.sleep(3)
            hotel_name = hotel.text
            hotel.click()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)
#            try:
#                hotel_name = self.driver.find_element_by_xpath("//h1[@class='detail-baseinfo_name  hotelTag-title_h1']").text
#            except Exception:
#                hotel_name = "N/A"
            try:
                hotel_stars = len(self.driver.find_elements_by_class_name("u-icon.u-icon-diamond.detail-baseinfo_title_level"))
            except Exception:
                hotel_stars = "N/A"
            room_link_xpath = "//span[@data-id='detail-room-list']"

            print("Clicking on Room tab..")
            self.driver.find_element_by_xpath(room_link_xpath).click()
            try:
                room_type = self.driver.find_elements_by_class_name("roomname")[0].text
            except Exception:
                room_type = "N/A"
            try:
                bed = self.driver.find_element_by_xpath("//*[2]/*[@class='salecard-bedfacility' and 1]/*[@class='bed' and 2]/*[@class='bed-content' and 2]/*[@class='underline' and 1]").text
            except Exception:
                bed = "N/A"
            try:
                facility = self.driver.find_element_by_xpath("//*[2]/*[@class='salecard-bedfacility' and 1]/*[@class='facility' and 3]/*[@class='des-with-icon' and 1]/*[@class='desc-text' and 1]").text
            except Exception:
                facility = "N/A"
            try:
                price = self.driver.find_element_by_class_name("note").text
            except:
                price = "N/A"
            print(str(hotel_name),end="\n")
            print(str(hotel_stars),end="\n")
            print(str(room_type),end="\n")
            print(str(bed),end="\n")
            print(str(facility),end="\n")
            print(str(price), end="\n")

            ws = workbook.get_worksheet_by_name("Hotelinfo")
            ws.write(workbook_row_index, workbook_column_index, destination)
            ws.write(workbook_row_index, workbook_column_index+1, check_in_date)
            ws.write(workbook_row_index, workbook_column_index+2, check_out_date)
            stripped_nights = re.sub("[^0-9^.]", "", nights)
            ws.write(workbook_row_index, workbook_column_index+3, stripped_nights)
            split_guest = guestinfo.split(", ")[1]
            stripped_guestinfo = re.sub("[^0-9^.]", "", split_guest)
            ws.write(workbook_row_index, workbook_column_index+4, stripped_guestinfo)
            ws.write(workbook_row_index, workbook_column_index+5, hotel_name)
            ws.write(workbook_row_index, workbook_column_index+6, hotel_stars)
            ws.write(workbook_row_index, workbook_column_index+7, room_type)
            ws.write(workbook_row_index, workbook_column_index+8, bed)
            ws.write(workbook_row_index, workbook_column_index+9, facility)
            stripped_price = re.sub("[^0-9^.]", "", price)
            ws.write(workbook_row_index, workbook_column_index+10, stripped_price)
            workbook_row_index+=1
            self.driver.close()
        return workbook
    def quit_browser(self):
        self.driver.quit()



