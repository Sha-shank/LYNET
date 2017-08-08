import wx
import wikipedia
import wolframalpha
import subprocess
import threading
import speech_recognition as sr


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,
            pos = wx.DefaultPosition,size=wx.Size(450,100),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
            wx.CLOSE_BOX | wx.CLIP_CHILDREN,
            title="LYNET")
       
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,label="Hello I am LYNET,your Virtual Assistant. How can I help you?")
        my_sizer.Add(lbl,0,wx.ALL,5)
        self.txt = wx.TextCtrl(panel,style=wx.TE_PROCESS_ENTER,size=(500,100))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER,self.OnEnter)
        my_sizer.Add(self.txt,0,wx.ALL,5)
        panel.SetSizer(my_sizer)
        self.Show()

    
         
    def OnEnter(self, event):
        input =self.txt.GetValue()
        input = input.lower()
        if input == '':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                self.txt.SetValue(r.recognize_google(audio))
                input =self.txt.GetValue()
                input = input.lower()
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understant audio")
            except sr.RequestError as e:
                print("Could not request resluts from Google Speech Recognition services {0}".format(e))

       
        try:
            #wolframalpha
            app_id = "H9GVPU-24L26AVY25"
            client = wolframalpha.Client(app_id)
            res = client.query(input)
            answer = next(res.results).text
            print("\nLYNET wol: " +answer+"\n\n")
            thread1 = threading.Thread(target=txttsp(answer))
            thread1.start()
                     
        except:
            #wikipedia
            rqans = wikipedia.summary(input, sentences=5, chars=0, auto_suggest=True, redirect=True)
            rqans = rqans.replace(u'\u2013','?')
            rqans = rqans.replace(u'\u2014','??')
            print "\nLYNET wiki: "+rqans+"\n"
            rqans = rqans.replace('\n','...')
            thread1 = threading.Thread(target=txttsp(rqans))
            thread1.start()
    
           
def txttsp(text):
        subprocess.call('espeak "'+ text+'"',shell=True)            

if __name__ == "__main__":
    app = wx.App(True)
    frame=MyFrame()
    app.MainLoop()
