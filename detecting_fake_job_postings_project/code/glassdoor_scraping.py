from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def get_jobs(job_keyword, num_jobs, location_keyword = None):
    """
    Gathers jobs as a dataframe, scraped from Glassdoor
    """

    # initialize the webdriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1120, 1000)
    url = 'https://www.glassdoor.com/Job/index.htm'
    driver.get(url)

    # search for the job keyword
    search_job = driver.find_element(by='id', value='searchBar-jobTitle')
    search_job.send_keys(job_keyword)
    search_job.send_keys(Keys.RETURN)

    # search for the jocation keyword if it was added
    if location_keyword is not None:
        search_location = driver.find_element(by='id', value='searchBar-location')
        search_location.send_keys(location_keyword)
        search_location.send_keys(Keys.RETURN)
    # get the list of all jobs
    jobs = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__JBBUV")
    time.sleep(1)

    # create a list to append the jobs into and an incremental variable to stop scraping
    jobs_list = []
    job_number = 1
    progress = []

    while job_number < num_jobs:  # if true, should be still looking for new jobs
        print(job_number) # for debugging
        # Progress variable is a list containing job numbers,
        # Sometime a program can run into a 'no such element' error and get stuck, so the last two
        # records in the progress_variables list will be the same.
        # In this case the job_number variable will be updated to the previous value to click on the next job.
        progress.append(job_number)
        if len(progress) >= 2 and progress[-1] == progress[-2]:
            job_number += 1
        # Steps:
        # 1. go over the job card on the left column and click on each, close the signup prompt if it appears
        try:
            job = jobs[job_number]
            try:
                job.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                driver.find_element(By.CLASS_NAME, 'CloseButton').click() # close the signup prompt
                time.sleep(1)
            except NoSuchElementException:
                time.sleep(1)
                pass

            # 2. click 'Show More' button to see the whole job description
            try:
                driver.find_element(By.CLASS_NAME, 'JobDetails_showMore__j5Z_h').click()
                time.sleep(1)
            except NoSuchElementException:
                job.click()
                print('#ERROR: no such element')
                time.sleep(30)
                driver.find_element(By.CLASS_NAME, 'JobDetails_showMore__j5Z_h').click()
            except ElementNotInteractableException:
                job.click()
                driver.implicitly_wait(30)
                print('#ERROR: not interactable')
                driver.find_element(By.CLASS_NAME, 'JobDetails_showMore__j5Z_h').click()

            # 3. scrape necessary data: company_name, location, job_title, job_description and salary_estimate
            company_name = job.find_element(By.CLASS_NAME, 'EmployerProfile_profileContainer__d5rMb').text
            location = job.find_element(By.CLASS_NAME, 'JobCard_location__N_iYE').text
            job_title = driver.find_element(By.CLASS_NAME, 'JobDetails_jobTitle__Rw_gn').text
            try:
                job_description = driver.find_element(By.CLASS_NAME, 'JobDetails_jobDescriptionWrapper__BTDTA').text
            except:
                job_description = None
            try:
                salary_estimate = job.find_element(By.CLASS_NAME, 'JobCard_salaryEstimate___m9kY').text
            except:
                salary_estimate = None

            # 4. add the job to jobs_list list and increment the job_number variable
            jobs_list.append({"site": 'Glassdoor',
                              "role": job_title,
                              "company_name": company_name,
                              "job_description": job_description,
                              "location": location,
                              "salary_estimate": salary_estimate})

            job_number += 1

        # 5. when you've reached the last job of the collumn
        # click on 'Show more jobs' button to load more jobs and replace the jobs list with the updated one
        except:
            try:
                driver.find_element(By.CLASS_NAME, 'JobsList_buttonWrapper__haBp5').click()
                time.sleep(10)
                jobs = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__JBBUV")
                time.sleep(1)
            except ElementClickInterceptedException:
                # close the signup popup if it appears
                driver.find_element(By.CLASS_NAME, 'CloseButton').click()
                jobs = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__JBBUV")
                time.sleep(1)
            except NoSuchElementException:
                # break the loop if there is no 'Show more jobw' button
                time.sleep(2)
                break


    # convert the list of jobs into a pandas DataFrame.
    return pd.DataFrame(jobs_list)


# This line will open a new chrome window and start the scraping.
df = get_jobs('Data Scientist', 300, 'United States')
df.to_csv('data.csv')
