from flask import Flask, render_template, request, redirect, url_for, flash
import os
import numpy as np
import time
import html
from PIL import Image

# ========================== Fungsionalitas compress image ==========================
def simultaneous_power_iteration(A, k):
  n, m = A.shape
  Q = np.random.rand(n, k)
  Q, _ = np.linalg.qr(Q)
  Q_prev = Q

  for i in range(200):
    Z = A.dot(Q)
    Q, R = np.linalg.qr(Z)

    err = ((Q - Q_prev) ** 2).sum()
    Q_prev = Q
    if err < 1e-3:
      break

  return np.abs(np.diag(R)), Q

# Algoritma SVD
def SVD(Matrix, k):
  # 0 < compressionRate < 1
  width, height = np.shape(Matrix)
  # k = compressionRate * min(width, height)
  Matrix_R = Matrix @ np.transpose(Matrix)
  SIG, U = simultaneous_power_iteration(Matrix_R, int(k))
  uRow, uWidth = U.shape
  
  U_2 = np.pad(U, ((0,0), (0, height - uWidth)))
  SIG = np.sqrt(SIG)
  SIG = np.diag(SIG)
  SIGRow, SIGWidth = SIG.shape
  SIG_2 = np.pad(SIG, ((0, height - SIGRow), (0, width - SIGWidth)))

  if (np.linalg.det(SIG) == 0):
    return Matrix

  VT = np.linalg.inv(SIG) @ np.transpose(U) @ Matrix
  VTHeight, VTWidth = VT.shape
  VT_2 = np.pad(VT, ((0, width - VTHeight), (0,0)))
  return np.clip(U_2 @ SIG_2 @ VT_2, 0, 255)

def compressImage(filename, img, compressionRate):
  with Image.open(img, mode="r") as im:
    hasAlpha = False # Cek jika memiliki alpha channel.
    oldFormat = None
    if (im.mode == 'P'):
      oldFormat = 'P'
      im = im.convert('RGBA')
    elif (im.mode == 'L'):
      oldFormat = 'L'
      im = im.convert('RGB')
    elif (im.mode == 'LA'):
      oldFormat = 'LA'
      im = im.convert('RGBA')
    channels = Image.Image.split(im)
    R = np.asarray(channels[0]).astype(float)
    G = np.asarray(channels[1]).astype(float)
    B = np.asarray(channels[2]).astype(float)
    if (len(channels) > 3):
      # Ada channel alpha; hasAlpha = true
      hasAlpha = True
      A = channels[3]
    
    imFinal = np.dstack((R,G,B)).astype(np.uint8)
    imFinal = Image.fromarray(imFinal)
      
    svdR = SVD(R, compressionRate)
    svdG = SVD(G, compressionRate)
    svdB = SVD(B, compressionRate)
    
    if (hasAlpha):
      IM_matr = np.dstack((svdR, svdG, svdB, A)).astype(np.uint8)
    else:
      IM_matr = np.dstack((svdR, svdG, svdB)).astype(np.uint8)
    
    IM_Final = Image.fromarray(np.uint8(IM_matr))
    if (oldFormat != None):
      IM_Final = IM_Final.convert(oldFormat)
    IM_Final.save(f'static/compressed/{filename}')
# ========================== End of fungsionalitas compress image ==========================

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "POST":
    if request.files:
      image = request.files["image"]
      if image.filename == '':
        flash('No selected file!')
        return redirect('/')
      if not allowed_file(image.filename):
        flash(f'Extension {os.path.splitext(image.filename)[1]} is not supported!')
        return redirect('/')
      image.save(os.path.join(UPLOAD_FOLDER, image.filename))
      imgName = os.path.splitext(image.filename)[0]
      imgExt = os.path.splitext(image.filename)[1]
      return redirect(f'/display/{imgName}/{imgExt}')

  return render_template('index.html')

@app.route('/display/<filename>/<ext>')
def display(filename, ext):
  imgPath = url_for('static', filename=f'uploads/{filename}{ext}')
  compressPath = f'/compress/{filename}/{ext}/loading'
  return render_template('display.html', imgPath=imgPath, compressPath=compressPath)

@app.route('/compress/<filename>/<ext>/<ctime>', methods=["GET", "POST"])
def compress(filename, ext, ctime):
  if request.method == 'POST':
    k = request.form.get('k')
    start_time = time.time()
    compressImage(f'{filename}{ext}', f"static/uploads/{filename}{ext}", k)
    duration = round(time.time() - start_time, 2)
    return redirect(f'/compress/{filename}/{ext}/{duration}')
  origPath = f'static/uploads/{html.unescape(filename)}{ext}'
  compressedPath = f'static/compressed/{html.unescape(filename)}{ext}'

  # Menghitung pixel difference percentage 
  i1 = Image.open(origPath)
  if (i1.mode == 'P'):
    i1 = i1.convert('RGBA')
  elif (i1.mode == 'L'):
    i1 = i1.convert('RGB')
  elif (i1.mode == 'LA'):
    i1 = i1.convert('RGBA')
  i2 = Image.open(compressedPath)
  if (i2.mode == 'P'):
    i2 = i2.convert('RGBA')
  elif (i2.mode == 'L'):
    i2 = i2.convert('RGB')
  elif (i2.mode == 'LA'):
    i2 = i2.convert('RGBA')
  pairs = zip(i1.getdata(), i2.getdata())
  if len(i1.getbands()) == 1:
      # for gray-scale jpegs
      dif = sum(abs(p1-p2) for p1,p2 in pairs)
  else:
      dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
  
  origPath = url_for('static', filename=f'uploads/{filename}{ext}')
  compressedPath = url_for('static', filename=f'compressed/{filename}{ext}')
  ncomponents = i1.size[0] * i1.size[1] * 3
  diffPercentage = round((dif / 255.0 * 100) / ncomponents, 2)
  return render_template('compress.html', origPath=origPath, compressedPath=compressedPath, time=ctime, diffPercentage=diffPercentage)

if __name__ == "__main__":
  app.run(debug=True)