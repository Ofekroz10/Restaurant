<h2>Resaturant Simulator</h2>    

<a href="https://ibb.co/1Lm1TVD"><img src="https://i.ibb.co/KXrdWZM/client.png" alt="client" border="0"></a>   
*Client screen*    
    
    
This project written by **Python**, using:    
<ul>
  <li>Multithreading</li>
  <li>Socket</li>
  <li>Tkinter</li>
  <li>Json and text files</li>
</ul>

<h2>Introduction</h2>

The goal of the project is to simulate a restaurant:   
   
**Client screen:** The application allow unlimited clients that work parallel. The client order meals, and you see the bill before    
you pay, then you click pay and the order send to the kitchen. the kitchen is the 'magic' of the application.    
*Order priority*: 3 Levels of priority: VIP, PLUS, NORMAL. The queue implements by binary heap, so the waiting queue that you can see   
in server screen is unordered, but always the queue pop the next order, by priority. 
   
**Server screen:** The server works behind the science. You can see the output of the server: 3 queues
<ul>
  <li>*Wating orders:* The orders that wait for treatment, there is limit number of workers, the workers work parallel but each worker   
  can treat only one order parallel</li>
  <li>*In kitchen:* each order has treatement time, dependent on the ingridients of each meals. When the order done, the worker start   
  working on the next order</li>
  <li>*Done*: The orders that waiting for collection. After timeout the order disappear</li>
</ul>

<a href="https://ibb.co/5Bj00KX"><img src="https://i.ibb.co/V2C11w0/server.png" alt="server" border="0"></a>

**Parallel, the server allow unlimited client to connect to the system.    
The application using these 3 queues in synchronize way.**

<h2>Settings</h2>    
By default the number of the workers in the kitchen is 2. If you want to set another value, open back.py and change the value of this varible      
   
```python
WORKERS = 2
```
The ingridients of each meals represents in a file text, for exmaple 'burget.txt', you can add or remove an ingridient. Just use this format   
```python
ING 1
ING 2
ING 3
....
```
To add new ingridient, just add it to the json file (ing.json)   
```python 
{"name":"ing_name", "price":x, "sec":y} # X, Y are numbers
```

<h2>How to use this project? <\h2>
First, run back.py this is the server, you will see the kitchen screen.
Then, run main_client.py. You can run unlimited times this file, this is the client.
