import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

class TCASEngineeringScraper:
    def __init__(self):
        self.data = []
        self.processing_data = []  # New list to store processing information
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Remove this line if you want to see the browser
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("Chrome driver initialized successfully")
        except Exception as e:
            print(f"Error initializing Chrome driver: {e}")
            print("Please make sure ChromeDriver is installed and in PATH")
            self.driver = None
    
    def search_engineering_programs(self, keywords):
        """Search for engineering programs using specific keywords"""
        if not self.driver:
            print("Driver not available")
            return []
        
        search_results = []
        
        for keyword in keywords:
            print(f"\nSearching for: {keyword}")
            try:
                # Navigate to TCAS search page
                self.driver.get("https://course.mytcas.com")
                time.sleep(3)
                
                # Find search box and enter keyword
                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='วิชา'], input[type='text']"))
                )
                search_box.clear()
                search_box.send_keys(keyword)
                search_box.send_keys(Keys.RETURN)
                
                # Wait for results to load
                time.sleep(5)
                
                # Find all course links
                course_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='course'], a[href*='program']")
                
                for link in course_links:
                    try:
                        course_url = link.get_attribute("href")
                        course_title = link.text.strip()
                        
                        # Filter for engineering programs only
                        if course_url and course_title and any(eng_word in course_title.lower() for eng_word in ['วิศวกรรม', 'engineering', 'วศ.บ']):
                            search_results.append({
                                'title': course_title,
                                'url': course_url,
                                'keyword': keyword
                            })
                            print(f"Found: {course_title}")
                    except Exception as e:
                        continue
                
                print(f"Found {len([r for r in search_results if r['keyword'] == keyword])} results for {keyword}")
                time.sleep(2)
                
            except Exception as e:
                print(f"Error searching for {keyword}: {e}")
                continue
        
        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()
        for result in search_results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        print(f"\nTotal unique programs found: {len(unique_results)}")
        return unique_results
    
    def extract_processing_info(self, course_url):
        """Extract processing information from course page for immediate saving"""
        try:
            print(f"Extracting processing info from: {course_url}")
            self.driver.get(course_url)
            time.sleep(3)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            processing_info = {}
            
            # Get full page text for pattern matching
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Extract course name
            try:
                course_name_selectors = [
                    "h1", "h2", ".course-name", ".program-name", 
                    "[class*='title']", "[class*='name']", ".course-title"
                ]
                
                for selector in course_name_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text and len(text) > 10:  # Assume course name is longer than 10 chars
                            processing_info['หลักสูตร'] = text
                            break
                    if 'หลักสูตร' in processing_info:
                        break
                
                if 'หลักสูตร' not in processing_info:
                    processing_info['หลักสูตร'] = "N/A"
                    
            except Exception as e:
                processing_info['หลักสูตร'] = "N/A"
            
            # Extract university name
            try:
                uni_selectors = [
                    ".university-name", ".institution-name", 
                    "[class*='university']", "[class*='institution']",
                    ".school-name", "[class*='school']"
                ]
                
                for selector in uni_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text and ('มหาวิทยาลัย' in text or 'university' in text.lower() or 'สถาบัน' in text):
                            processing_info['มหาวิทยาลัย'] = text
                            break
                    if 'มหาวิทยาลัย' in processing_info:
                        break
                
                # Also try to find university name in page text
                if 'มหาวิทยาลัย' not in processing_info:
                    uni_pattern = r'([^.\n]*(?:มหาวิทยาลัย|สถาบัน)[^.\n]*)'
                    matches = re.findall(uni_pattern, page_text)
                    if matches:
                        for match in matches:
                            if len(match.strip()) < 100:  # Reasonable length
                                processing_info['มหาวิทยาลัย'] = match.strip()
                                break
                
                if 'มหาวิทยาลัย' not in processing_info:
                    processing_info['มหาวิทยาลัย'] = "N/A"
                    
            except Exception as e:
                processing_info['มหาวิทยาลัย'] = "N/A"
            
            # Extract ประเภทหลักสูตร (Course Type)
            try:
                course_type_patterns = [
                    r'ประเภทหลักสูตร[:\s]*([^\n]+)',
                    r'ประเภท[:\s]*([^\n]+)',
                    r'(ภาษาไทย|ภาษาอังกฤษ|นานาชาติ|ปกติ|พิเศษ|บางเวลา|เต็มเวลา)',
                    r'(ปกติ|พิเศษ|นานาชาติ|International|Regular|Special)'
                ]
                
                course_type_found = False
                for pattern in course_type_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    if matches:
                        # Get the most relevant match
                        for match in matches:
                            if len(match.strip()) < 50:  # Reasonable length
                                processing_info['ประเภทหลักสูตร'] = match.strip()
                                course_type_found = True
                                break
                        if course_type_found:
                            break
                
                if not course_type_found:
                    processing_info['ประเภทหลักสูตร'] = "N/A"
                    
            except Exception as e:
                processing_info['ประเภทหลักสูตร'] = "N/A"
            
            # Extract ค่าใช้จ่าย (Detailed cost information)
            try:
                cost_patterns = [
                    r'ค่าใช้จ่าย[:\s]*([^\n]+)',
                    r'อัตราค่าเรียน[:\s]*([^\n]+)',
                    r'อัตราค่าลำเรียน[:\s]*([^\n]+)',
                    r'ค่าเทอม[:\s]*([^\n]+)',
                    r'ค่าธรรมเนียม[:\s]*([^\n]+)',
                    r'(\d+(?:,\d+)*\s*(?:บาท|บ\.)[^\n]*(?:เทอม|ภาค|ปี|หลักสูตร))',
                    r'(อัตราค่า[^\n]*\d+(?:,\d+)*[^\n]*บาท)',
                    r'(ค่าลำเรียน[^\n]*\d+(?:,\d+)*[^\n]*บาท)'
                ]
                
                cost_info = []
                for pattern in cost_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    if matches:
                        for match in matches:
                            if len(match.strip()) < 200:  # Reasonable length
                                cost_info.append(match.strip())
                
                if cost_info:
                    # Remove duplicates and join
                    unique_costs = list(set(cost_info))
                    processing_info['ค่าใช้จ่าย'] = ' | '.join(unique_costs[:3])  # Limit to top 3
                else:
                    processing_info['ค่าใช้จ่าย'] = "N/A"
                    
            except Exception as e:
                processing_info['ค่าใช้จ่าย'] = "N/A"
            
            # Add URL for reference
            processing_info['URL'] = course_url
            
            return processing_info
            
        except Exception as e:
            print(f"Error extracting processing info: {e}")
            return {
                'หลักสูตร': "N/A",
                'มหาวิทยาลัย': "N/A",
                'ประเภทหลักสูตร': "N/A",
                'ค่าใช้จ่าย': "N/A",
                'URL': course_url
            }
    
    def extract_course_details(self, course_url):
        """Extract detailed information from course page"""
        try:
            print(f"Extracting details from: {course_url}")
            self.driver.get(course_url)
            time.sleep(3)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            course_info = {}
            
            # Extract course name
            try:
                course_name_selectors = [
                    "h1", "h2", ".course-name", ".program-name", 
                    "[class*='title']", "[class*='name']"
                ]
                
                for selector in course_name_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text and len(text) > 10:  # Assume course name is longer than 10 chars
                            course_info['course_name'] = text
                            break
                    if 'course_name' in course_info:
                        break
                
                if 'course_name' not in course_info:
                    course_info['course_name'] = "N/A"
                    
            except Exception as e:
                course_info['course_name'] = "N/A"
            
            # Extract university name
            try:
                uni_selectors = [
                    ".university-name", ".institution-name", 
                    "[class*='university']", "[class*='institution']"
                ]
                
                for selector in uni_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text and ('มหาวิทยาลัย' in text or 'university' in text.lower()):
                            course_info['university'] = text
                            break
                    if 'university' in course_info:
                        break
                
                if 'university' not in course_info:
                    course_info['university'] = "N/A"
                    
            except Exception as e:
                course_info['university'] = "N/A"
            
            # Extract tuition fee
            try:
                # Get all text content from the page
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                
                # Look for fee information
                fee_patterns = [
                    r'ค่าเทอม[:\s]*(\d+(?:,\d+)*)\s*บาท',
                    r'ค่าใช้จ่าย[:\s]*(\d+(?:,\d+)*)\s*บาท',
                    r'อัตราค่าเทอม[:\s]*(\d+(?:,\d+)*)\s*บาท',
                    r'(\d+(?:,\d+)*)\s*บาท[/\s]*เทอม',
                    r'(\d+(?:,\d+)*)\s*บาท[/\s]*ปี'
                ]
                
                fee_found = False
                for pattern in fee_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    if matches:
                        course_info['tuition_fee'] = matches[0]
                        fee_found = True
                        break
                
                if not fee_found:
                    course_info['tuition_fee'] = "N/A"
                    
            except Exception as e:
                course_info['tuition_fee'] = "N/A"
            
            return course_info
            
        except Exception as e:
            print(f"Error extracting course details: {e}")
            return None
    
    def parse_tuition_fee(self, fee_text, page_context=""):
        """Parse tuition fee text and convert to per-semester amount"""
        if not fee_text or fee_text == "N/A":
            return None
        
        try:
            # Remove commas and extract numbers
            amount = int(fee_text.replace(',', ''))
            
            # Determine if it's per year or per semester based on context
            if 'ปี' in page_context or 'year' in page_context.lower():
                amount = amount / 2  # Convert yearly to semester
            elif 'หลักสูตร' in page_context or 'program' in page_context.lower():
                amount = amount / 8  # Assume 4 years = 8 semesters
            # If no context, assume it's per semester
            
            return int(amount)
        
        except Exception as e:
            print(f"Error parsing fee: {fee_text} - {e}")
            return None
    
    def scrape_engineering_programs(self):
        """Main scraping function"""
        # Keywords to search for
        keywords = [
            "วิศวกรรมคอมพิวเตอร์",
            "วิศวกรรมปัญญาประดิษฐ์"
        ]
        
        print("=== Starting TCAS Engineering Programs Scraper ===")
        
        # Search for programs
        search_results = self.search_engineering_programs(keywords)
        
        if not search_results:
            print("No programs found")
            return []
        
        print(f"\n=== Processing {len(search_results)} programs ===")
        
        # Extract details for each program
        for i, result in enumerate(search_results, 1):
            print(f"\n[{i}/{len(search_results)}] Processing: {result['title']}")
            
            # Extract processing information first
            processing_info = self.extract_processing_info(result['url'])
            processing_info['ลำดับ'] = i
            processing_info['คำค้นหา'] = result['keyword']
            processing_info['ข้อมูลเริ่มต้น'] = result['title']
            
            # Add to processing data
            self.processing_data.append(processing_info)
            
            # Display the processing info
            print(f"มหาวิทยาลัย: {processing_info['มหาวิทยาลัย']}")
            print(f"หลักสูตร: {processing_info['หลักสูตร']}")
            print(f"ประเภทหลักสูตร: {processing_info['ประเภทหลักสูตร']}")
            print(f"ค่าใช้จ่าย: {processing_info['ค่าใช้จ่าย']}")
            print("-" * 50)
            
            # Extract detailed course information
            course_details = self.extract_course_details(result['url'])
            
            if course_details:
                # Parse tuition fee
                semester_fee = self.parse_tuition_fee(course_details['tuition_fee'])
                
                # Only include programs with valid fee <= 200,000
                if semester_fee and semester_fee <= 200000:
                    program_data = {
                        'มหาวิทยาลัย': course_details['university'],
                        'หลักสูตร': course_details['course_name'],
                        'ค่าเทอม_บาท': semester_fee,
                        'ค่าเทอม_ข้อมูลต้นฉบับ': course_details['tuition_fee'],
                        'URL': result['url'],
                        'คำค้นหา': result['keyword']
                    }
                    
                    self.data.append(program_data)
                    print(f"✓ Added: {course_details['university']} - {semester_fee:,} บาท/เทอม")
                
                elif semester_fee and semester_fee > 200000:
                    print(f"✗ Excluded (too expensive): {course_details['university']} - {semester_fee:,} บาท/เทอม")
                
                else:
                    print(f"✗ Excluded (no fee info): {course_details['university']}")
            
            else:
                print(f"✗ Failed to extract details")
            
            time.sleep(1)  # Be respectful to the server
        
        print(f"\n=== Scraping completed ===")
        print(f"Successfully scraped {len(self.data)} programs")
        print(f"Processing data collected for {len(self.processing_data)} programs")
        return self.data
    
    def save_to_excel(self, filename="tcas_engineering_programs.xlsx"):
        """Save scraped data to Excel file with multiple sheets"""
        if not self.data and not self.processing_data:
            print("No data to save")
            return None

        # Handle file permission issues
        import os
        from datetime import datetime

        # If file exists and can't be accessed, create a new filename
        if os.path.exists(filename):
            try:
                # Try to access the file
                with open(filename, 'r'):
                    pass
            except PermissionError:
                # Create a new filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = filename.replace('.xlsx', '')
                filename = f"{base_name}_{timestamp}.xlsx"
                print(f"Original file is in use. Saving to: {filename}")

        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Save processing data
                if self.processing_data:
                    processing_df = pd.DataFrame(self.processing_data)
                    processing_df.to_excel(writer, sheet_name='Processing_Data', index=False)
                    print(f"Processing data saved: {len(processing_df)} records")

                # Save main data
                if self.data:
                    df = pd.DataFrame(self.data)
                    df = df.sort_values('ค่าเทอม_บาท')
                    df.to_excel(writer, sheet_name='Main_Data', index=False)
                    print(f"Main data saved: {len(df)} records")

                    # Show summary
                    print(f"Average fee: {df['ค่าเทอม_บาท'].mean():,.0f} บาท/เทอม")
                    print(f"Cheapest: {df['ค่าเทอม_บาท'].min():,.0f} บาท/เทอม")
                    print(f"Most expensive: {df['ค่าเทอม_บาท'].max():,.0f} บาท/เทอม")

                    print(f"\n=== Data saved to {filename} ===")
                    return df
                else:
                    df = pd.DataFrame(self.processing_data)
                    print(f"\n=== Only processing data saved to {filename} ===")
                    return df

        except Exception as e:
            print(f"Failed to save file: {e}")
            return None


    
    def close(self):
        """Close the webdriver"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")

def main():
    """Main function to run the scraper"""
    scraper = TCASEngineeringScraper()
    
    if not scraper.driver:
        print("Failed to initialize driver. Please check ChromeDriver installation.")
        return
    
    try:
        # Scrape data
        data = scraper.scrape_engineering_programs()
        
        # Save to Excel (will save both processing and main data)
        df = scraper.save_to_excel()
        
        if df is not None and len(df) > 0:
            print("\n=== Sample of collected data ===")
            print(df[['มหาวิทยาลัย', 'หลักสูตร', 'ค่าเทอม_บาท']] if 'ค่าเทอม_บาท' in df.columns else df.head())
        else:
            print("No final data available, but processing data has been saved")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()