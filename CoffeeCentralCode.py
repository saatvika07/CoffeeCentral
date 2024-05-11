from tkinter import * 
from tkinter import scrolledtext 
from tkinter import messagebox 
import folium 
import webbrowser 
import tkinter as tk  
import pygame 
from folium.plugins import AntPath 
 
pygame.mixer.init() # using mixer from pygame 
 
def play_sound(): 
    sound_path =  "C:\\Users\\Murthy\\Downloads\\kwise.mp3"  
    pygame.mixer.music.load(sound_path) #to load music 
    pygame.mixer.music.play() #to play music 
 
def main_win_destroy(): 
    main_win.destroy() 
 
def close_input_win(): 
    input_win.destroy() 
 
def check_inputs(): 
    try: 
        global dx, dy, n, q 
        dx = int(dx_entry.get()) 
        dy = int(dy_entry.get()) 
        n = int(n_entry.get()) 
        q = int(q_entry.get()) 
        global coffee_shops, queries 
        coffee_shops = [list(map(int, shop.split())) for shop in 
shops_entry.get("1.0", END).split("\n") if shop.strip()] 
        queries = [int(query) for query in queries_entry.get("1.0", 
END).split("\n") if query.strip()] 
        if dx == 0 and dy == 0 or n == 0 or q == 0: 
            messagebox.showerror("Error", "Please enter valid non-zero values.") 
        else: 
            check_coffee_shop_locations() 
             
 
    except ValueError: 
        messagebox.showerror("Error", "Please enter valid integer values.") 
 
def check_coffee_shop_locations(): 
    global max_coffee_shops_list 
    global optimal_location_list 
    optimal_location_list = [] 
    max_coffee_shops_list = [] 
 
    for coordinates in coffee_shops: 
        x,y = coordinates 
        if (x not in range(0,dx+1)) or (y not in range(0,dy+1)):   #condition to 
check whether the coffee shop locations are within the dx,dy values or not. 
            messagebox.showerror("Error", "Please enter valid coffee shop 
locations.") 
    global output_dict 
    output_dict=dict() 
    for dis in queries: 
        max_coffee_shops, optimal_location,nearby_coffee_shops= 
find_optimal_location(dis) 
        optimal_location_list.append(optimal_location) 
        max_coffee_shops_list.append(max_coffee_shops) 
        output_dict[optimal_location] = nearby_coffee_shops 
 
    display_output_win() 
 
def display_output_win(): 
    output_win = Tk() 
    output_win.geometry("1500x1500") 
    output_win.title("Coffee Central") 
    output_win.configure(bg="burlywood") 
     
     
     
    output_str = "" 
    for i in range(len(max_coffee_shops_list)): 
        max_shops = max_coffee_shops_list[i] 
        op_loc = optimal_location_list[i] 
        output_str += f"Query distance: {queries[i]}\n" 
        output_str += f"Maximum reachable coffee shops: {max_shops}\n" 
        output_str += f"Optimal location: {op_loc}\n\n" 
 
    label1 = Label(output_win, text=output_str,font=("Courier 10 
Pitch",22),bg="burlywood") 
    label1.grid(row=0, column=0) 
 
    get_map_button =Button(output_win,text="Get map",font=("Courier 10 
Pitch",22),command = get_map) 
    get_map_button.place(relx=0.5, rely=0.5, anchor='se') 
    play_sound() 
 
    
 
def find_optimal_location(dis): 
    max_coffee_shops = 0 
    optimal_location = (0, 0) 
    for c in range(0, dx + 1): 
        for d in range(0, dy + 1): 
            total_coffee_shops = 0 
            for coordinate_list in coffee_shops: 
                a, b = coordinate_list 
                if abs(a - c) + abs(b - d) <= dis: 
                    total_coffee_shops += 1 
 
            if total_coffee_shops > max_coffee_shops: 
                max_coffee_shops = total_coffee_shops 
                optimal_location = (c, d) 
 
            elif total_coffee_shops == max_coffee_shops: 
                if d < optimal_location[1]: 
                    optimal_location = (c, d) 
                elif d == optimal_location[1] and c < optimal_location[0]: 
                    optimal_location = (c, d) 
    nearby_coffee_shops = [] 
    for coordinate_list in coffee_shops: 
        a, b = coordinate_list 
        if (abs(a - optimal_location[0]) + abs(b - optimal_location[1])) <= q: 
            nearby_coffee_shops.append(coordinate_list) 
 
    return max_coffee_shops, optimal_location, nearby_coffee_shops 
 
def get_map(): 
    #folium 
    # Create map centered on city coordinates 
    map_obj = folium.Map(location=(30,10),zoom_start=3) 
    play_sound() 
    # loop over shops and add markers with custom icon 
    for shop in coffee_shops: 
        folium.Marker(location=[shop[0], shop[1]],  
                icon=folium.Icon(color="darkred", 
                icon_color="white", 
                prefix="fa",icon="mug-saucer"), 
                tooltip = f"Coffee Shop at:({shop[0]},{shop[1]})" 
                ).add_to(map_obj) 
     
    for home in optimal_location_list: 
        folium.Marker(location=[home[0], home[1]], 
                      icon=folium.Icon(color="lightgray", 
                      icon_color="purple",prefix="fa", 
                      icon="house-chimney"), 
                      tooltip = f"Optimal location at:({home[0]},{home[1]})" 
                      ).add_to(map_obj) 
 
    # to create paths for optimal locations and nearby locations 
    #getting the points path 
    key1, val = None, None 
    pathlatlong = [] 
    color_list = ["red", "blue","green", "purple", "orange", "darkred", 
                    "lightred", "beige", "darkblue", "darkgreen", "cadetblue",  
                    "darkpurple", "white", "pink", "lightblue", "lightgreen",  
                    "gray", "black", "lightgray"] 
    i=0 
    for k, v in output_dict.items(): 
        key1, value_list = k, v 
        for val in value_list: 
            pathlatlong=[key1,val] 
            AntPath(pathlatlong,delay = 800,weight = 
8,color=color_list[i],dash_array=[30,15]).add_to(map_obj) 
        i+=1 
     
    #Save the map to a file and open it in a new tab in the web browser 
    # Save the map as an HTML file 
     
    map_obj.save("coffee_shops_map.html") 
     
    # Open the HTML file in a new browser window 
    webbrowser.open_new_tab("coffee_shops_map.html") 
 
# Main Window 
# Main Window 
main_win = Tk() 
main_win.geometry("825x832+250+25") 
main_win.title("Coffee Central") 
bg=PhotoImage(file="C:\\Users\\Murthy\\Desktop\\1.png") 
#bg=PhotoImage(file="C:\Users\chand\OneDrive\Pictures\wise2nd.png") 
bg_label=Label(main_win,image=bg) 
bg_label.place(x=0,y=0,relwidth=1,relheight=1) 
start_btn = Button(main_win, text="Continue..", font=("Courier 10 
Pitch",22),command=main_win_destroy) 
start_btn.place(relx=0.5, rely=0.6, anchor='center') 
main_win.mainloop() 
# Input Window 
input_win = Tk() 
input_win.geometry("1500x1500+25+20") 
input_win.title("Coffee Central") 
bg=PhotoImage(file="C:\\Users\\Murthy\\Desktop\\2 .png") 
bg_label=Label(input_win,image=bg) 
bg_label.place(x=0,y=0,relwidth=1,relheight=1) 
main_heading = Label(input_win, font=("Courier 10 Pitch",22), anchor="center") 
main_heading.grid(row=0, column=0) 
 
dx_btn = Label(input_win, text="Enter x coordinate of city", font=("Courier 10 
Pitch",22), anchor="w") 
dx_btn.grid(row=30, column=80, padx=15, pady=15) 
dx_entry = Entry(input_win,  font=("Courier 10 Pitch",22)) 
dx_entry.grid(row=30, column=90, padx=20, pady=20) 
 
dy_btn = Label(input_win, text="Enter y coordinate of city", font=("Courier 10 
Pitch",22), anchor="w") 
dy_btn.grid(row=50, column=80, padx=15, pady=15) 
dy_entry = Entry(input_win,  font=("Courier 10 Pitch",22)) 
dy_entry.grid(row=50, column=90, padx=20, pady=20) 
 
n_btn = Label(input_win, text="Enter number of coffee shops", font=("Courier 10 
Pitch",22), anchor="w") 
n_btn.grid(row=70, column=80, padx=15, pady=15) 
n_entry = Entry(input_win,  font=("Courier 10 Pitch",22)) 
n_entry.grid(row=70, column=90, padx=5, pady=10) 
 
shops_btn = Label(input_win, text="Enter coffee shop locations", font=("Courier 
10 Pitch",22), anchor="w") 
shops_btn.grid(row=90, column=80, padx=15, pady=15) 
shops_entry = scrolledtext.ScrolledText(input_win, font=("Courier 10 Pitch",22), 
height=3, width=20) 
shops_entry.grid(row=90, column=90, padx=5, pady=10) 
 
q_btn = Label(input_win, text="Enter number of queries", font=("Courier 10 
Pitch",22), anchor="w") 
q_btn.grid(row=110, column=80, padx=15, pady=15) 
q_entry = Entry(input_win,  font=("Courier 10 Pitch",22)) 
q_entry.grid(row=110, column=90, padx=5, pady=10) 
 
queries_btn = Label(input_win, text="Enter queries (one per line)", 
font=("Courier 10 Pitch",22), anchor="w") 
queries_btn.grid(row=130, column=80, padx=15, pady=15) 
queries_entry = scrolledtext.ScrolledText(input_win,  font=("Courier 10 
Pitch",22), height=3, width=20) 
queries_entry.grid(row=130, column=90, padx=5, pady=10) 
optimal_location_btn = Button(input_win, text="Find the optimal locations", 
font=("Courier 10 Pitch",22), anchor="center" , command=check_inputs) 
optimal_location_btn.grid(row=200, column=90) 
play_sound() 
input_win.mainloop() 
