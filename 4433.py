import tkinter
import customtkinter
#from msilib import RadioButtonGroup
from ssl import get_default_verify_paths
import tkinter as tk
from typing import Counter
import requests
from bs4 import BeautifulSoup
import numpy as np
from tkinter import Toplevel, messagebox
import tkinter.ttk as ttk
import webbrowser
import pandas as pd

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("360x630")
app.title("基金績效篩選工具")
    
def gui_inti():
    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    frame_2 = customtkinter.CTkFrame(master=app)
    frame_2.pack(pady=20, padx=60, fill="both", expand=True)
    
    label_1 = customtkinter.CTkLabel(text="初步篩選     4433法則",master=frame_1, justify=tkinter.LEFT).pack(pady=12, padx=10)
    global url_entry,url,new
    url= "https://www.sitca.org.tw/ROC/Industry/IN3200.aspx?PGMID=IN0302"
    new = 1
    button_instruction_3 = customtkinter.CTkButton(
    master= frame_1,
    command= openweb,
    text= "基金績效評比網站",
    border_color= "#608a4d", 
    hover_color= "#81b867",
    fg_color= "#79ae61").pack(pady=12, padx=10)
    url_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text="請提供資料來源網址")
    url_entry.pack(pady=12, padx=10)

    global optionmenu_1 
    optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["理柏", "晨星"])
    optionmenu_1.pack(pady=12, padx=10)
    optionmenu_1.set("選擇資料來源")
    
    button_instruction = customtkinter.CTkButton(
    master= frame_1,
    command= fftt_instruction,
    text= "什麼是4433法則?",
    border_color= "#9e4a43", 
    hover_color= "#e06a61",
    fg_color= "#c75d55").pack(pady=12, padx=10)
    
    button_instruction_2 = customtkinter.CTkButton(
    master= frame_1,
    command= fftt_instruction,
    text= "操作說明",
    border_color= "#9e4a43", 
    hover_color= "#e06a61",
    fg_color= "#c75d55").pack(pady=12, padx=10)

    

    
    button_1 = customtkinter.CTkButton(text="送出",master=frame_1, command=crawler)
    button_1.pack(pady=12, padx=10)
 
    label_2 = customtkinter.CTkLabel(text="進階篩選     風險指標",master=frame_2).pack(pady=12, padx=10)
    global optionmenu_3,optionmenu_2,select_sort
    optionmenu_3 = customtkinter.CTkOptionMenu(master=frame_2, values=["夏普", "標準差","Beta","Alpha"])
    optionmenu_3.set("選擇風險指標")
    optionmenu_3.pack(pady=12, padx=10)
    optionmenu_2 = customtkinter.CTkOptionMenu(master=frame_2, values=["大到小", "小到大"])
    optionmenu_2.set("風險指標呈現方式")
    optionmenu_2.pack(pady=12, padx=10)
        

    

    app.mainloop()
    
def openweb():
        webbrowser.open(url,new=new)  
def fftt_instruction():
    print("我還不想寫")
    
    
global get_list   
get_list = []

def crawler ():


    resp = requests.get(url_entry.get(), verify=False)
    global select_type

    data_index_=[]
    data_index_morningstar = [1,4,5,6,7,8,9,10,12,13,14,15]
    data_index_lipper = [1,4,5,6,7,8,9,10,12,13,14,16]

    if optionmenu_1.get() == "晨星":
        data_index = data_index_morningstar
        select_type =1
    else:
        data_index = data_index_lipper
        select_type =0

    
    soup = BeautifulSoup(resp.text, 'html.parser')
    rows_even = soup.find_all(class_ = "DTeven")
    rows_odd = soup.find_all(class_ = "DTodd")

    delete_list = []
    #初始化
    even_data=[['\xa0' for count in range(12)] for row in range(len(rows_even))]
    odd_data=[['\xa0' for count in range(12)] for row in range(len(rows_odd))]
    


    i = 0
    count = 0
    #讀取偶數欄資料
    for row_even in rows_even:
        count = 0
        for y in range(12):
            even_data[i][y]=row_even.find_all('td')[data_index[count]].text
            if even_data[i][y] == '\xa0':
                delete_list.append(i)
            count+=1
        i+=1

    #刪除空格資料
    even_data = np.delete(even_data,delete_list, axis = 0)
    delete_list.clear()

    i = 0
    count = 0
    #讀取奇數欄資料
    for row_odd in rows_odd:
        count = 0
        for y in range(12):
            odd_data[i][y]=row_odd.find_all('td')[data_index[count]].text
            if odd_data[i][y] == '\xa0':
                delete_list.append(i)
            count+=1
        i+=1

    odd_data = np.delete(odd_data,delete_list, axis = 0)
    #合併資料
    global data
    data = np.vstack((even_data,odd_data)) 
    run(data,select_type)

def run(data,select_type):
    if(select_type==1):#晨星
        df = pd.DataFrame(data, columns=['Name', '3m', '6m', '1y', '2y', '3y', '5y', 'YTD','sd','sharpe','alpha','beta'])
        df[[ '3m', '6m', '1y', '2y', '3y', '5y', 'YTD','sd','sharpe','alpha','beta']] = df[[ '3m', '6m', '1y', '2y', '3y', '5y', 'YTD','sd','sharpe','alpha','beta']].apply(pd.to_numeric)
    else:
        df = pd.DataFrame(data, columns=['Name', '3m', '6m', '1y', '2y', '3y', '5y', 'YTD','sd','beta','sharpe','alpha'])
        df[[ '3m', '6m', '1y', '2y', '3y', '5y', 'YTD','sd','beta','sharpe','alpha']] = df[[ '3m', '6m', '1y', '2y', '3y', '5y', 'YTD','sd','beta','sharpe','alpha']].apply(pd.to_numeric)
      
 
    thresholds_1q = df[['1y', '2y', '3y', '5y', 'YTD']].quantile(0.75)  # 75top 25% performance for the year columns
    thresholds_1t = df[['3m', '6m']].quantile(0.67)  # 67top 33% performance for the month columns



    df['4433'] = ((df['3m'] >= thresholds_1t['3m']) & (df['6m'] >= thresholds_1t['6m'])) & \
                ((df['1y'] >= thresholds_1q['1y']) & (df['2y'] >= thresholds_1q['2y']) & \
                (df['3y'] >= thresholds_1q['3y']) & (df['5y'] >= thresholds_1q['5y']) & \
                (df['YTD'] >= thresholds_1q['YTD']))
    global adv_data 
    adv_data = df[df['4433']]
    
    global names_str
    name_list = []
    
    for fund_name in df[df['4433']]['Name']:
       name_list.append(fund_name)
    names_str = '\n'.join(name_list)
    if(df['4433'].sum()!=0):
        fftt_result_toplevel()  
        column_to_sort = ""

        if(optionmenu_3.get() == "夏普"):
            column_to_sort = 'sharpe'
        elif(optionmenu_3.get() == "標準差"):
            column_to_sort = 'sd'
        elif(optionmenu_3.get() == "Beta"):
            column_to_sort = 'beta'
        elif(optionmenu_3.get() == "Alpha"):
            column_to_sort = 'alpha'
        global result_data
        result_data = []
        tmpdata = []
        if(optionmenu_2.get()=="大到小"):
            sort_type = False
        else:
            sort_type = True
        if column_to_sort:
            final = df[df['4433']].sort_values(by=column_to_sort, ascending=sort_type)
            for fund_name in final['Name']:
                tmpdata.append(fund_name)
                 
        result_data = '\n'.join(tmpdata)
    else:
        tk.messagebox.showerror(title=None, message='無符合資料')
def fftt_result_toplevel():
        window = customtkinter.CTkToplevel()
        window.title("4433篩選結果")
        window.geometry("530x400")
        label_2 = customtkinter.CTkLabel(window, text ="以下基金為4433法則後篩選後之結果")
   
        label_1 = customtkinter.CTkLabel(window, text =names_str)
        label_1.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        button = customtkinter.CTkButton(text="進階篩選",master=window, command=tmp).pack()

def final_result(result_data):
        window = customtkinter.CTkToplevel()
        window.title("進階篩選結果")
        window.geometry("530x400")
        label_1 = customtkinter.CTkLabel(window, text =''.join(result_data))
        label_1.pack(side="top", fill="both", expand=True, padx=40, pady=40)  
    
def tmp():
    final_result(result_data)


  

    


if __name__ =='__main__':
    gui_inti()


