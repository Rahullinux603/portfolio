from flask import Flask, render_template, request, session, flash, send_file
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import mysql.connector
import base64, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/ServerLogin')
def ServerLogin():
    return render_template('ServerLogin.html')


@app.route('/VerifierLogin')
def VerifierLogin():
    return render_template('VerifierLogin.html')


@app.route('/NewVerifier')
def NewVerifier():
    return render_template('NewVerifier.html')


@app.route("/slogin", methods=['GET', 'POST'])
def slogin():
    if request.method == 'POST':
        if request.form['uname'] == 'server' and request.form['password'] == 'server':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM crimenaltb  ")
            data = cur.fetchall()
            return render_template('ServerHome.html', data=data)

        else:
            flash("UserName or Password Incorrect!")
            return render_template('ServerLogin.html')



@app.route("/ServerHome")
def ServerHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM crimenaltb  ")
    data = cur.fetchall()
    return render_template('ServerHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            return render_template('SenderHome.html')

        else:
            flash("UserName or Password Incorrect!")
            return render_template('AdminLogin.html')





@app.route("/ReceiverInfo")
def ReceiverInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM recivertb  ")
    data = cur.fetchall()
    return render_template('ReceiverInfo.html', data=data)


@app.route("/MessageInfo")
def MessageInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM msgtb  ")
    data = cur.fetchall()
    return render_template('MessageInfo.html', data=data)


@app.route("/newcrime", methods=['GET', 'POST'])
def newcrime():
    if request.method == 'POST':
        name = request.form['name']
        Height = request.form['Height']
        Weight = request.form['Weight']
        Mole = request.form['Mole']
        Colour = request.form['Colour']
        CrimeInfo = request.form['CrimeInfo']
        import random
        file = request.files['file']
        file.save("static/upload/" + file.filename)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM msgtb ")
        data = cursor.fetchone()

        if data:
            mid = float(data[0]) + 1

        else:
            mid = 1
            return 'Incorrect username / password !'

        cid ="CRIMRNALID00"+str(mid)


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into crimenaltb values('','"+ cid +"','" + name + "','" + Height + "','" + Weight + "','" + Mole + "','" + Colour + "','" + CrimeInfo + "','"+
            file.filename+"')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('SenderHome.html')


@app.route('/CrimeInfo')
def CrimeInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM crimenaltb  ")
    data = cur.fetchall()
    return render_template('CrimeInfo.html', data=data)

@app.route("/down")
def down():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM crimenaltb where  id ='" + id + "'")
    data2 = cursor.fetchone()
    if data2:
        aadhar = data2[8]
        return send_file('static/upload/' + aadhar, as_attachment=True)


@app.route("/Remove")
def Remove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from crimenaltb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Criminal  info Remove Successfully!')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM crimenaltb   ")
    data = cur.fetchall()
    return render_template('CrimeInfo.html', data=data)


@app.route('/SenderHome')
def SenderHome():
    return render_template('SendMessage.html')


@app.route('/SendMessage')
def SendMessage():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT username FROM recivertb  ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT CriminalId FROM crimenaltb  ")
    data1 = cur.fetchall()
    return render_template('SendMessage.html', data=data,data1=data1)


@app.route("/imupload", methods=['GET', 'POST'])
def imupload():
    if request.method == 'POST':
        from stegano import lsb
        from PIL import Image

        rname = request.form['rname']
        hinfo = request.form['hinfo']
        hkey = request.form['hkey']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)
        image = Image.open("./static/upload/" + savename)
        print(f"Original size : {image.size}")  # 5464x3640
        sunset_resized = image.resize((400, 400))
        sunset_resized.save("./static/upload/" + savename)

        hidedata = hinfo

        secret = lsb.hide("./static/upload/" + savename, hidedata)

        pathname, extension = os.path.splitext("./static/upload/" + savename)
        filename = pathname.split('/')
        imageName = filename[-1] + ".png"
        sname = filename[-1]
        secret.save("./static/Encode/" + imageName)

        savedir = 'static/Split/'
        filename = "./static/Encode/" + imageName
        img = Image.open(filename)
        width, height = img.size
        start_pos = start_x, start_y = (0, 0)
        cropped_image_size = w, h = (200, 200)

        frame_num = 1
        for col_i in range(0, width, w):
            for row_i in range(0, height, h):
                crop = img.crop((col_i, row_i, col_i + w, row_i + h))
                save_to = os.path.join(savedir, sname + "_{:02}.png")
                crop.save(save_to.format(frame_num))
                frame_num += 1

        session["rname"] = rname
        session["ssname"] = sname
        session["hkey"] = hkey
        flash('Hide Data & Split Image Successfully!')

        return render_template('SSplitInfo.html', iname=savename, sname=sname)


@app.route("/mncrypt", methods=['GET', 'POST'])
def mncrypt():
    if request.method == 'POST':
        rname = session["rname"]
        sname = session["ssname"]
        hkey = session["hkey"]
        savename = sname + ".png"
        secp_k = generate_key()
        privhex = secp_k.to_hex()
        pubhex = secp_k.public_key.format(True).hex()

        filepath1 = "./static/Split/" + sname + "_01.png"
        filepath2 = "./static/Split/" + sname + "_02.png"
        filepath3 = "./static/Split/" + sname + "_03.png"
        filepath4 = "./static/Split/" + sname + "_04.png"

        newfilepath1 = "./static/Encrypt/" + sname + "_01.png"
        newfilepath2 = "./static/Encrypt/" + sname + "_02.png"
        newfilepath3 = "./static/Encrypt/" + sname + "_03.png"
        newfilepath4 = "./static/Encrypt/" + sname + "_04.png"

        data1 = 0
        data2 = 0
        data3 = 0
        data4 = 0

        with open(filepath1, "rb") as File:
            data1 = base64.b64encode(File.read())  # convert binary to string data to read file

        with open(filepath2, "rb") as File:
            data2 = base64.b64encode(File.read())

        with open(filepath3, "rb") as File:
            data3 = base64.b64encode(File.read())
        with open(filepath4, "rb") as File:
            data4 = base64.b64encode(File.read())

        print("Private_key:", privhex, "\nPublic_key:", pubhex, "Type: ", type(privhex))

        if privhex == 'null':
            flash('Please Choose Another File,file corrupted!')
            return render_template('SendMessage.html')

        else:
            encrypted_secp = encrypt(pubhex, data1)
            with open(newfilepath1, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data2)
            with open(newfilepath2, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data3)
            with open(newfilepath3, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data4)
            with open(newfilepath4, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM recivertb where  UserName='" + rname + "'")
            data = cursor.fetchone()

            if data:
                email = data[3]


            else:
                return 'Incorrect username / password !'

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO msgtb VALUES ('','" + rname + "','" + email + "','" + sname + "','" + savename + "','" + hkey + "','" + pubhex + "','" + privhex + "')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id) FROM msgtb ")
            data = cursor.fetchone()

            if data:
                mid = data[0]

            else:
                return 'Incorrect username / password !'
            msg = "Hide Id " + str(mid) + " UnhideKey " + str(hkey) + " PrivateKey " + str(privhex)

            sendmail(email, msg)

            flash("Encrypt and Send key Successfully!")
            return render_template('SSplitInfo.html', iname=savename, sname=sname, pvkey=privhex)


@app.route('/SMessageInfo')
def SMessageInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM msgtb ")
    data = cur.fetchall()
    return render_template('SMessageInfo.html', data=data)


@app.route("/newreceiver", methods=['GET', 'POST'])
def newreceiver():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into recivertb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")
    return render_template('NewVerifier.html')


@app.route("/Verifierlogin", methods=['GET', 'POST'])
def Verifierlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['rname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from recivertb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('ReceiverLogin.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM recivertb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('ReceiverHome.html', data=data)


@app.route('/ReceiverHome')
def ReceiverHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT username FROM sendertb  where username='" + session['rname'] + "' ")
    data = cur.fetchall()
    return render_template('SendMessage.html', data=data)


@app.route('/RMessageInfo')
def RMessageInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM msgtb where ReceiverName='" + session['rname'] + "'  ")
    data = cur.fetchall()
    return render_template('RMessageInfo.html', data=data)


@app.route("/vdecrypt")
def vdecrypt():
    id = request.args.get('id')
    session["rhcid"] = id
    return render_template('HDecrypt.html')


@app.route("/imdecrypt", methods=['GET', 'POST'])
def imdecrypt():
    if request.method == 'POST':

        prikey = request.form['prikey']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM msgtb where  id='" + session["rhcid"] + "'")
        data = cursor.fetchone()

        if data:
            imid = data[3]
            tpriKey = data[7]

        else:
            return 'Incorrect username / password !'

        if prikey == tpriKey:

            filepath1 = "./static/Encrypt/" + imid + "_01.png"
            filepath2 = "./static/Encrypt/" + imid + "_02.png"
            filepath3 = "./static/Encrypt/" + imid + "_03.png"
            filepath4 = "./static/Encrypt/" + imid + "_04.png"

            newfilepath1 = "./static/Decrypt/" + imid + "_01.png"
            newfilepath2 = "./static/Decrypt/" + imid + "_02.png"
            newfilepath3 = "./static/Decrypt/" + imid + "_03.png"
            newfilepath4 = "./static/Decrypt/" + imid + "_04.png"

            data1 = 0
            data2 = 0
            data3 = 0
            data4 = 0

            privhex = tpriKey

            with open(filepath1, "rb") as File:
                data1 = base64.b64decode(File.read())

            decrypted_secp = decrypt(privhex, data1)

            with open(newfilepath1, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            with open(filepath2, "rb") as File:
                data2 = base64.b64decode(File.read())

            decrypted_secp = decrypt(privhex, data2)

            with open(newfilepath2, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            with open(filepath3, "rb") as File:
                data3 = base64.b64decode(File.read())
            decrypted_secp = decrypt(privhex, data3)
            with open(newfilepath3, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            with open(filepath4, "rb") as File:
                data4 = base64.b64decode(File.read())
            decrypted_secp = decrypt(privhex, data4)
            with open(newfilepath4, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            flash('Decrypt Successfully all images')
            return render_template('Hmerge.html', sname=imid)



        else:

            flash('Your private key  Incorrect!')
            return render_template('HDecrypt.html')


@app.route("/mergeim", methods=['GET', 'POST'])
def mergeim():
    if request.method == 'POST':
        from PIL import Image
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM msgtb where  id='" + session["rhcid"] + "'")
        data = cursor.fetchone()

        if data:
            imid = data[3]

        else:
            return 'Incorrect username / password !'

        files = [
            "./static/Decrypt/" + imid + "_01.png",
            "./static/Decrypt/" + imid + "_02.png",
            "./static/Decrypt/" + imid + "_03.png",
            "./static/Decrypt/" + imid + "_04.png"]

        result = Image.new("RGB", (400, 400))

        for index, file in enumerate(files):
            path = os.path.expanduser(file)
            img = Image.open(path)
            img.thumbnail((200, 200), Image.ANTIALIAS)
            x = index // 2 * 200
            y = index % 2 * 200
            w, h = img.size
            print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
            result.paste(img, (x, y, x + w, y + h))

        result.save(os.path.expanduser('static/merge/' + imid + '.png'))
        mimage = 'static/merge/' + imid + '.png'
        flash('Successfully Merge Image!')

        return render_template('HDView.html', iname=mimage)


@app.route("/hvdown", methods=['GET', 'POST'])
def hvdown():
    if request.method == 'POST':
        uhkey = request.form['hkey']

        from stegano import lsb

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM msgtb where  id='" + session["rhcid"] + "'")
        data = cursor.fetchone()

        if data:
            imid = data[3]
            hKey = data[5]

        else:
            return 'Incorrect username / password !'

        if uhkey == hKey:
            flash('Successfully Unhide Message!')
            clear_message = lsb.reveal('static/merge/' + imid + '.png')
            mimage = 'static/merge/' + imid + '.png'
            session['mimage'] = mimage
            print(clear_message)

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crimenaltb  where CriminalId='" + clear_message + "'")
            data = cursor.fetchone()

            if data:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='1securecrimedb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM crimenaltb  where CriminalId='" + clear_message + "'  ")
                data = cur.fetchall()
                return render_template('ViewCrimeInfo.html', data=data)
            else:
                flash('Hide Information Incorrect!')
                return render_template('HDView.html', iname=mimage, pre=clear_message)


        else:
            mimage = 'static/merge/' + imid + '.png'
            flash('Your Unhide key  Incorrect!')
            return render_template('HDView.html', iname=mimage)


def sendmail(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "sampletest685@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "hneucvnontsuwgpj")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
