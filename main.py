from scraping_classes.browseraction import BrowserAction


url = 'https://www.trip.com/hotels/list?city=1&countryId=1&checkin=2020/11/18&checkout=2020/11/25&optionId=1&optionType=City&directSearch=0&display=Beijing&crn=1&adult=2&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1'

BA = BrowserAction()
trip_excel_file = BA.create_workbook()
BA.get_site(url)
BA.scroll_until_load_button_displayed()
wb = BA.get_hotel_info(trip_excel_file)
wb.close()
BA.quit_browser()