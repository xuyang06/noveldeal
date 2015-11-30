import smtplib  
from email.mime.text import MIMEText  
#mailto_list=["xuyang06@gmail.com"] 
mail_host=  
mail_user=   
mail_pass=    
#mail_user="noveldealcom"   
#mail_pass="myufo06!"  
mail_postfix=
  
def send_mail(to_list, sub, content):  
	me="Novel Deal Team"+"<"+mail_user+"@"+mail_postfix+">"   
	msg = MIMEText(content,_subtype='html',_charset='gb2312')    
	msg['Subject'] = sub    
	msg['From'] = me  
	msg['To'] = ";".join(to_list)  
	try:  
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.ehlo()
		s.starttls()
		s.login(mail_user, mail_pass)  
		s.sendmail(me, to_list, msg.as_string())  
		s.close()  
		return True  
	except Exception, e:  
		print str(e)  
		return False

def write_mail_content(query_res, user_name):
    content = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"></link> \
	            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css"></link> \
	            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script> \
	            <div class="col-lg-8 col-lg-offset-2"> \
	            <h2>Hi, ' + user_name + '! How are you? Check out the deals below that we found for you!\
	            </h2>\
	            <div class="col-lg-8 col-lg-offset-2"> '
	#<td width="61%" valign="top" align="center"> \
    #        	<div align="left"> \
    #        	<ul style="display:none">
    for query in query_res:
        #print query
	       #content += '<li style="height: 25px !important;"> \
			#	<table border="0" width="300"> \
			#	<tr> \
			#	<td height="0" align="center"> \
			#	<b> \
			#	<a href="' + query['href'] + '"> \
			#	<font face="Verdana, Arial, Helvetica, sans-serif"> \
			#	<font color=#ff0000 size=1> \
			#	Super Hot, ' + query['product'] + '@' + query['brand'] + '\
			#	</font> \
			#	</font>\
			#	</a>\
			#	</b>\
			#	</td>\
			#	</tr>\
			#	</table>\
			#	</li>'
        content += '<b> \
                    <font face="times new roman"> \
                    <p> \
                    Super Hot, ' + str("{0:.0f}%".format((1.0-query['off']) * 100)) + 'off@' \
                    + '<a href="' + query['href'] + '">' + query['brand'] + ' ' + query['product'] +\
                    '</a> \
                    </p> \
                    </font> \
                    </b>'
                    
    content += '</div>'            
	#content += '</ul></div></td>'
    return content

if __name__ == '__main__':
    mailto_list = ["xuyang06@gmail.com"] 
    content = [{'off': 0.3, 'brand':'Prada', 'href':'a', 'product':'abc'}, \
               {'off': 0.3, 'brand':'Prada', 'href':'ab', 'product':'abcd'}, \
               {'off': 0.3, 'brand':'Prada', 'href':'av', 'product':'abce'}]
    user_name = 'Yang Xu' 
    #print write_mail_content(content, user_name)
    if send_mail(mailto_list,"hello", write_mail_content(content, user_name)):  
        print "send successful!"  
    else:  
        print "failure!" 