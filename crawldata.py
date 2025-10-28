import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

chrome_options = Options()
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

POST_URL = "https://www.facebook.com/share/p/15C8WnWFdX/"

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    driver.get(POST_URL)
    
    print("Đã mở trình duyệt. Bạn có 05s để đăng nhập...")
    time.sleep(5)

    NUM_ATTEMPTS = 50
    print(f"Bắt đầu tải bình luận ({NUM_ATTEMPTS} lượt)...")

    def safe_click(element):
        try:
            driver.execute_script("arguments[0].click();", element)
            return True
        except WebDriverException:
            return False

    for i in range(NUM_ATTEMPTS):
        print(f" Lượt {i+1}/{NUM_ATTEMPTS}")
        try:
            more_btns = driver.find_elements(By.XPATH, "//div[@role='button'][contains(., 'more comment') or contains(., 'Xem thêm') or contains(., 'Xem thêm bình luận')]")
            for b in more_btns:
                if safe_click(b):
                    time.sleep(0.6)
        except Exception:
            pass

        try:
            reply_btns = driver.find_elements(By.XPATH, "//span[contains(., 'replies') or contains(., 'trả lời') or contains(., 'Xem trả lời')]")
            for b in reply_btns:
                if safe_click(b):
                    time.sleep(0.4)
        except Exception:
            pass

        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
        except Exception:
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1.2)

    print("Hoàn tất tải bình luận, bắt đầu trích xuất...")

    scraped = []
    try:
        comment_blocks = driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'Comment') or contains(@aria-label, 'Bình luận')]")
        if comment_blocks:
            for cb in comment_blocks:
                try:
                    nodes = cb.find_elements(By.XPATH, ".//div[@dir='auto']")
                    text = " ".join([n.text.strip() for n in nodes if n.text.strip()])
                    if text and len(text) > 5:
                        scraped.append(text)
                except Exception:
                    continue
        else:
            elems = driver.find_elements(By.XPATH, "//div[@dir='auto']")
            for e in elems:
                t = e.text.strip()
                if t and len(t) > 20:
                    scraped.append(t)
    except Exception as e:
        print("Lỗi khi trích xuất:", e)

    if not scraped:
        print("Không thu thập được bình luận. Kiểm tra link/đăng nhập/selectors.")
    else:
        new_df = pd.DataFrame({"raw_text": scraped}).drop_duplicates().reset_index(drop=True)
        out = "ictu_post_comments.csv"
        if os.path.exists(out):
            try:
                old_df = pd.read_csv(out, encoding="utf-8-sig")
                combined = pd.concat([old_df, new_df], ignore_index=True)
                combined = combined.drop_duplicates().reset_index(drop=True)
            except Exception:
                combined = new_df
        else:
            combined = new_df
        combined.to_csv(out, index=False, encoding="utf-8-sig")
        print(f"Đã lưu tổng {len(combined)} mẫu vào {out}")
        
except Exception as e:
    print(f"Lỗi: {str(e)}")
finally:
    try:
        driver.quit()
    except:
        pass