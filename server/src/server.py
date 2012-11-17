import web, json #@UnresolvedImport

urls = (
  '/', 'hello')

app = web.application(urls, globals(), True)

render = web.template.render('templates/')

class hello:
    
    def GET(self):
        return render.hello("Templates demo", "Hello", "A long time ago...")
    
    def POST(self):
        data = web.data()
        d = json.loads(data)
#        print type(d) #sanity check
        lastAdded = d[2][len(d[2])-2] #index last value added from entire RRD
        fo = open('serverData.txt','a')
        fo.write('Time: ' + str(d[0][1]) + '    Data: ' + str(lastAdded) + '\n')
        fo.close()
        return "****Data Posted****" #YAY!

if __name__ == "__main__":
    app.run()