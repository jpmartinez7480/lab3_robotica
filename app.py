def sexadecimal_to_decimal(list_values):
    seconds = list_values[2]/60
    minutes = (list_values[1]+seconds)/60
    return list_values[0]+(-1*minutes)

def get_coordinates_lat_or_long(value,v,option):
    if option == 1:
        seconds = v/30.92
    elif option == 2:
        seconds = v/29.36
    predata = value.split(".")
    minutes = (float(predata[1])/(10**len(predata[1])))*60
    aux_seg = str(minutes).split(".")
    seg = ((float(aux_seg[1])/(10**len(aux_seg[1])))*60)+seconds
    return [int(predata[0]),int(aux_seg[0]),seg]


def get_is_going_right(long1):
    list_coordinates_long = get_coordinates_lat_or_long(str(long1),-5,2)
    return sexadecimal_to_decimal(list_coordinates_long)

def get_is_going_down(lat1,lat2):
    list_coordinates_route = []
    while lat1 > lat2:
        list_coordinates_lat = get_coordinates_lat_or_long(str(lat1),5,1)
        lat1 = sexadecimal_to_decimal(list_coordinates_lat)
        if lat1 < lat2:
            return list_coordinates_route
        else:
            list_coordinates_route.append(lat1)
    return list_coordinates_route

def get_interest_point(obj1):
    height = float(obj1[4])
    weight = float(obj1[3])
    latitude = obj1[0]
    longitude = obj1[1]
    data_lat1_obj_avoid = get_coordinates_lat_or_long(latitude,(-height/2)-1,1)
    data_long1_obj_avoid = get_coordinates_lat_or_long(longitude,(weight/2)+1,2)
    data_lat2_obj_avoid = get_coordinates_lat_or_long(latitude,(height/2)+1,1)
    data_long2_obj_avoid = get_coordinates_lat_or_long(longitude,(-weight/2)-1,2)
    value = sexadecimal_to_decimal(data_lat1_obj_avoid)
    value2 = sexadecimal_to_decimal(data_long1_obj_avoid)
    value3 = sexadecimal_to_decimal(data_lat2_obj_avoid)
    value4 = sexadecimal_to_decimal(data_long2_obj_avoid)
    first_interest_point = [value,value2]
    second_interest_point = [value3,value2]
    thirth_interest_point = [value,value4]
    fourth_interest_point = [value3,value4]
    return [first_interest_point,second_interest_point,thirth_interest_point,fourth_interest_point]

def avoid_obstacles(interest_points,route,obj):
    new_routes = []
    i = 0
    j = 0
    while i < len(route):
        j = 0
        while j < len(route[i]):
            if route[i][j][1] > interest_points[0][1] and route[i][j][1] < interest_points[2][1] or route[i][j][1] > interest_points[1][1] and route[i][j][1] < interest_points[3][1]:
                data_lat_obj_avoid = route[i][j][0]
                data_lat_obj2_avoid = get_coordinates_lat_or_long(str(data_lat_obj_avoid),float(obj[4]),1) 
                data_long_obj_avoid = get_coordinates_lat_or_long(str(route[i][j][1]),float(obj[3])/2,2)
                data_lat2_obj_avoid = get_coordinates_lat_or_long(str(route[i][j][0]),float(obj[4]),1)
                data_long2_obj_avoid = get_coordinates_lat_or_long(str(route[i][j][1]),-float(obj[3])/2,2)
                
                data_long_res_avoid = sexadecimal_to_decimal(data_long_obj_avoid)
                data_lat2_res_avoid = sexadecimal_to_decimal(data_lat2_obj_avoid)
                data_long2_res_avoid = sexadecimal_to_decimal(data_long2_obj_avoid)
                data_lat_res_avoid = sexadecimal_to_decimal(data_lat_obj2_avoid)
                
                new_routes.append([data_lat2_res_avoid,data_long_res_avoid])
                new_routes.append([data_lat2_res_avoid,data_long_res_avoid])
                new_routes.append([data_lat_res_avoid,data_long2_res_avoid])
            else:
                new_routes.append(route[i][j])
            j+=1
        i+=1
    return new_routes

def make_route(list_coordinates):
    lat1 = float(list_coordinates[0][0])
    long1 = float(list_coordinates[0][1])
    lat2 = float(list_coordinates[1][0])
    long2 = float(list_coordinates[2][1])
    list_coordinates_route_right_down_up = []
    ###lat
    list_coordinates_route_down_up = get_is_going_down(lat1,lat2)
    list_coordinates_route_down_up.insert(0,lat1)
    list_coordinates_route_down_up.append(lat2)
    ###long
    while long1 < long2:
        long1 = get_is_going_right(long1)
        if long1 > long2:
            print("")
        else:
            list_coordinates_route_right_down_up.append(long1)
    list_coordinates_route_right_down_up.insert(0,float(list_coordinates[0][1]))
    list_coordinates_route_right_down_up.append(long2)
    geo = []
    for long in list_coordinates_route_right_down_up:
        aux = []
        for lat in list_coordinates_route_down_up:
            aux.append([lat,long])
        geo.append(aux)
        list_coordinates_route_down_up.reverse()
    return geo      

   
def write_file(list_coordinates,filename):
    file = open(filename, "w")
    file.write("QGC WPL 110")
    i = 0
    j = 1
    
    for e in list_coordinates:
        if j > 0:
            file.write(str(i)+"\t"+str(j)+"\t"+"0\t"+"16\t"+"0.0\t"+"0.0\t"+"0.0\t"+"0.0\t"+str(e[0])+"\t"+str(e[1])+"\t"+"5\t"+"1\n")
            j-=1
        file.write(str(i)+"\t"+"0"+"\t"+"0\t"+"16\t"+"0.0\t"+"0.0\t"+"0.0\t"+"0.0\t"+str(e[0])+"\t"+str(e[1])+"\t"+"5\t"+"1\n")
        i+=1
    file.close()




print("======= Los valores a ingresar separelos por un espacio =======")
square1 = input("Ingrese latitud y longitud esquina 1: ")
square2 = input("Ingrese latitud y longitud esquina 2: ")
square3 = input("Ingrese latitud y longitud esquina 3: ")
square4 = input("Ingrese latitud y longitud esquina 4: ")

obst = int(input("¿¿Cuantos obstaculos quiere agregar??: "))
i = 0
list_obst = []
while i < 0:
    ob1 = input("Ingrese latitud, longitud, altura, ancho, largo del obstaculo: ")
    list_obst.append(ob1)
    i+=1

square1_1 = square1.split(" ")
square2_2 = square2.split(" ")
square3_3 = square3.split(" ")
square4_4 = square4.split(" ")
area = [square1_1,square2_2,square3_3, square4_4]

filename = input("Ingrese nombre de archivo a guardar(con extension): ")
routes = make_route(area)
#write_file(routes,filename)
obj = ["-33.449651","-70.68964",8,10,10]
interest_points = get_interest_point(["-33.449651","-70.68964",8,10,10])
new_routes = avoid_obstacles(interest_points,routes,obj)
write_file(new_routes,filename) 
