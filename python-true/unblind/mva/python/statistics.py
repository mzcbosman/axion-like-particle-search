import math
from ROOT import Math, TF1, TMinuit, gRandom
from array import array

class Uncertainty:
  def __init__(self, value=None, *args):
    self.value = 0.
    self.error = 0.
    try:
      self.value = float(value.value)
      try:
        self.error = (float(value.error[0]), float(value.error[1]))
      except:
        self.error = float(value.error)
    except AttributeError:
      if value != None:
        self.value = float(value)
        if len(args) == 1:
          try:
            self.error = (abs(float(args[0][0])), abs(float(args[0][1])))
          except:
            self.error = abs(float(args[0]))
        else:
          error = 0.0
          for arg in args:
            error += float(arg)**2
          self.error = math.sqrt(error)

  def isAsymmetric(self):
    return isinstance(self.error, tuple)

  def getError(self):
    return self.error

  def getErrorHigh(self):
    if self.isAsymmetric():
      return self.error[1]
    else:
      return self.error

  def getErrorLow(self):
    if self.isAsymmetric():
      return self.error[0]
    else:
      return self.error

  def sample(self):
    if not self.isAsymmetric():
      if self.error == 0:
        return self.value
      return gRandom.Gaus(self.value, self.error)

    val = gRandom.Gaus()
    if val < 0:
      return val*self.error[0] + self.value;
    return val*self.error[1] + self.value;

  def __str__(self):
    if self.isAsymmetric():
      return str(self.value) + ' + ' + str(self.error[1]) + ' - ' + str(self.error[0]);
    return str(self.value) + ' +/- ' + str(self.error);    

  def __repr__(self):
    if self.isAsymmetric():
      return 'Uncertainty:\t' + str(self.value) + ' + ' + str(self.error[1]) + ' - ' + str(self.error[0]);
    return 'Uncertainty:\t' + str(self.value) + ' +/- ' + str(self.error);

  def __iadd__(self, value):    
    try:
      self.value += value.value
      if self.isAsymmetric():
        if value.isAsymmetric():
          self.error = (math.sqrt(self.error[0]**2 + value.error[0]**2), math.sqrt(self.error[1]**2 + value.error[1]**2))
        else:
          self.error = (math.sqrt(self.error[0]**2 + value.error**2), math.sqrt(self.error[1]**2 + value.error**2))
      else:
        if value.isAsymmetric():
          self.error = (math.sqrt(self.error**2 + value.error[0]**2), math.sqrt(self.error**2 + value.error[1]**2))
        else:
          self.error = math.sqrt(self.error**2 + value.error**2)
    except AttributeError:
      self.value += value
    return self

  def __add__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          error = (math.sqrt(self.error[0]**2 + value.error[0]**2), math.sqrt(self.error[1]**2 + value.error[1]**2))
        else:
          error = (math.sqrt(self.error[0]**2 + value.error**2), math.sqrt(self.error[1]**2 + value.error**2))
      else:
        if value.isAsymmetric():
          error = (math.sqrt(self.error**2 + value.error[0]**2), math.sqrt(self.error**2 + value.error[1]**2))
        else:
          error = math.sqrt(self.error**2 + value.error**2)
      return Uncertainty(self.value + value.value, error)
    except AttributeError:
      return Uncertainty(self.value + value, self.getError())

  def __radd__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          error = (math.sqrt(self.error[0]**2 + value.error[0]**2), math.sqrt(self.error[1]**2 + value.error[1]**2))
        else:
          error = (math.sqrt(self.error[0]**2 + value.error**2), math.sqrt(self.error[1]**2 + value.error**2))
      else:
        if value.isAsymmetric():
          error = (math.sqrt(self.error**2 + value.error[0]**2), math.sqrt(self.error**2 + value.error[1]**2))
        else:
          error = math.sqrt(self.error**2 + value.error**2)
      return Uncertainty(self.value + value.value, error)
    except AttributeError:
      return Uncertainty(self.value + value, self.getError())


  def __isub__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          self.error = (math.sqrt(self.error[0]**2 + value.error[1]**2), math.sqrt(self.error[1]**2 + value.error[0]**2))
        else:
          self.error = (math.sqrt(self.error[0]**2 + value.error**2), math.sqrt(self.error[1]**2 + value.error**2))
      else:
        if value.isAsymmetric():
          self.error = (math.sqrt(self.error**2 + value.error[1]**2), math.sqrt(self.error**2 + value.error[0]**2))
        else:
          self.error = math.sqrt(self.error**2 + value.error**2)
    except AttributeError:
      self.value -= value
    return self

  def __sub__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          error = (math.sqrt(self.error[0]**2 + value.error[1]**2), math.sqrt(self.error[1]**2 + value.error[0]**2))
        else:
          error = (math.sqrt(self.error[0]**2 + value.error**2), math.sqrt(self.error[1]**2 + value.error**2))
      else:
        if value.isAsymmetric():
          error = (math.sqrt(self.error**2 + value.error[1]**2), math.sqrt(self.error**2 + value.error[0]**2))
        else:
          error = math.sqrt(self.error**2 + value.error**2)
      return Uncertainty(self.value - value.value, error)
    except AttributeError:
      return Uncertainty(self.value - value, self.getError())

  def __rsub__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          error = (math.sqrt(self.error[1]**2 + value.error[0]**2), math.sqrt(self.error[0]**2 + value.error[1]**2))
        else:
          error = (math.sqrt(self.error[1]**2 + value.error**2), math.sqrt(self.error[0]**2 + value.error**2))
      else:
        if value.isAsymmetric():
          error = (math.sqrt(self.error**2 + value.error[0]**2), math.sqrt(self.error**2 + value.error[1]**2))
        else:
          error = math.sqrt(self.error**2 + value.error**2)
      return Uncertainty(value.value - self.value, error)
    except AttributeError:
      return Uncertainty(value - self.value, (self.error[1], self.error[0]))

  def __imul__(self, value):
    try:
      self.error = math.sqrt(self.error**2*value.value**2 + value.error**2*self.value**2)
      self.value *= value.value
    except AttributeError:
      self.value *= value
      self.error *= value
      self.error = abs(self.error)
    return self

  def __mul__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          return Uncertainty(self.value*value.value, (math.sqrt(self.error[0]**2*value.value**2 + value.error[0]**2*self.value**2), math.sqrt(self.error[1]**2*value.value**2 + value.error[1]**2*self.value**2)))
        else:
          return Uncertainty(self.value*value.value, (math.sqrt(self.error[0]**2*value.value**2 + value.error**2*self.value**2), math.sqrt(self.error[1]**2*value.value**2 + value.error**2*self.value**2)))
      else:
        if value.isAsymmetric():
          return Uncertainty(self.value*value.value, (math.sqrt(self.error**2*value.value**2 + value.error[0]**2*self.value**2), math.sqrt(self.error**2*value.value**2 + value.error[1]**2*self.value**2)))
        else:
          return Uncertainty(self.value*value.value, math.sqrt(self.error**2*value.value**2 + value.error**2*self.value**2))
    except AttributeError:
      if self.isAsymmetric():
        return Uncertainty(self.value*value, (abs(self.error[0]*value),abs(self.error[1]*value)))
      else:
        return Uncertainty(self.value*value, abs(self.error*value))

  def __rmul__(self, value):
    try:
      return Uncertainty(self.value*value.value, math.sqrt(self.error**2*value.value**2 + value.error**2*self.value**2))
    except AttributeError:
      return Uncertainty(self.value*value, abs(self.error*value))


  def __idiv__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          self.error = (math.sqrt(self.error[0]**2/value.value**2 + value.error[0]**2*self.value**2/value.value**4), math.sqrt(self.error[0]**2/value.value**2 + value.error[1]**2*self.value**2/value.value**4))
        else:
          self.error = (math.sqrt(self.error[0]**2/value.value**2 + value.error**2*self.value**2/value.value**4), math.sqrt(self.error[0]**2/value.value**2 + value.error**2*self.value**2/value.value**4))
      else:
        if value.isAsymmetric():
          self.error = (math.sqrt(self.error**2/value.value**2 + value.error[0]**2*self.value**2/value.value**4), math.sqrt(self.error**2/value.value**2 + value.error[1]**2*self.value**2/value.value**4))
        else:
          self.error = math.sqrt(self.error**2/value.value**2 + value.error**2*self.value**2/value.value**4)
      self.value /= value.value
    except AttributeError:
      if self.isAsymmetric():
        self.value /= value
        self.error = (abs(self.error[0]/value), abs(self.error[1]/value))
      else:
        self.value /= value
        self.error /= value
        self.error = abs(self.error)
    return self

  def __div__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          return Uncertainty(self.value/value.value, (math.sqrt(self.error[0]**2/value.value**2 + value.error[0]**2*self.value**2/value.value**4), math.sqrt(self.error[0]**2/value.value**2 + value.error[1]**2*self.value**2/value.value**4)))
        else:
          return Uncertainty(self.value/value.value, (math.sqrt(self.error[0]**2/value.value**2 + value.error**2*self.value**2/value.value**4), math.sqrt(self.error[0]**2/value.value**2 + value.error**2*self.value**2/value.value**4)))
      else:
        if value.isAsymmetric():
          return Uncertainty(self.value/value.value, (math.sqrt(self.error**2/value.value**2 + value.error[0]**2*self.value**2/value.value**4), math.sqrt(self.error**2/value.value**2 + value.error[1]**2*self.value**2/value.value**4)))
        else:
          return Uncertainty(self.value/value.value, math.sqrt(self.error**2/value.value**2 + value.error**2*self.value**2/value.value**4))
    except AttributeError:
      if self.isAsymmetric():
        return Uncertainty(self.value/value, (abs(self.error[0]/value), abs(self.error[1]/value)))
      return Uncertainty(self.value/value, abs(self.error/value))

  def __rdiv__(self, value):
    try:
      if self.isAsymmetric():
        if value.isAsymmetric():
          return Uncertainty(value/value*self.value, (math.sqrt(value.error[0]**2/self.value**2 + self.error[0]**2*value.value**2/self.value**4), math.sqrt(value.error[1]**2/self.value**2 + self.error[1]**2*value.value**2/self.value**4)))
        return Uncertainty(value/value*self.value, (math.sqrt(value.error**2/self.value**2 + self.error[0]**2*value.value**2/self.value**4), math.sqrt(value.error**2/self.value**2 + self.error[1]**2*value.value**2/self.value**4)))

      if value.isAsymmetric():
        return Uncertainty(value/value*self.value, (math.sqrt(value.error[0]**2/self.value**2 + self.error**2*value.value**2/self.value**4), math.sqrt(value.error[1]**2/self.value**2 + self.error**2*value.value**2/self.value**4)))
      return Uncertainty(value/value*self.value, math.sqrt(value.error**2/self.value**2 + self.error**2*value.value**2/self.value**4))
    except AttributeError:
      if self.isAsymmetric():
        return Uncertainty(value/self.value, (abs(self.error[0]*value/self.value**2), abs(self.error[1]*value/self.value**2)))
      return Uncertainty(value/self.value, abs(self.error*value/self.value**2))

  def __float__(self):
    return float(self.value)

def mean(values, rms=False):
  if not values:
    return Uncertainty(0,0)
  xbar  = 0
  x2bar = 0
  for value in values:
    xbar += value
    x2bar += value*value
  N = float(len(values))
  xbar /= N
  x2bar /= N
  if rms:
    return Uncertainty(xbar, math.sqrt(x2bar - xbar*xbar))
  return Uncertainty(xbar, math.sqrt((x2bar - xbar*xbar)/(N-1)))

class Average:
  def __init__(self):
    self.__V  = None
    self.__V2 = None
    self.__N  = 0
    self.__cache = None

  def __iadd__(self, value):    
    self.add(value)
    return self

  def add(self, value):
    self.__cache = None
    if self.__N == 0:
      self.__V  = value
      self.__V2 = value*value
    else:
      self.__V  += value
      self.__V2 += value*value
    self.__N += 1

  def __compute__(self):
    if self.__cache:
      return
    if self.__N > 0:
      N = float(self.__N)
      mean = self.__V/N
      rms  = math.sqrt(self.__V2/N - mean*mean)
      meanerr = rms/math.sqrt(N)
      self.__cache = (mean, rms, meanerr, N)
    else:
      self.__cache = (0,0,0,0)

  def uncertainty(self):
    self.__compute__()
    return Uncertainty(self.__cache[0], self.__cache[2])

  def mean(self):
    self.__compute__()
    return self.__cache[0]

  def rms(self):
    self.__compute__()
    return self.__cache[1]

  def meanerr(self):
    self.__compute__()
    return self.__cache[2]

  def N(self):
    self.__compute__()
    return self.__cache[3]


def efficiency(trials, result, conf=0.683, bays = True):

  def interval(x):
    if math.isnan(x): return 2
#    r = Math.BrentRootFinder()
    r = Math.Roots.Bisection()
    f = TF1("intfunc", "TMath::BetaIncomplete(x,[2],[3]) - TMath::BetaIncomplete([0],[2],[3]) - [1]", x, 1.01)
    f.SetParameter(0, x)
    f.SetParameter(1, conf)
    f.SetParameter(2, result + 1)
    f.SetParameter(3, trials - result + 1)
    w = Math.WrappedTF1(f)
    r.SetFunction(w, x, 1.01)
    if not r.Solve() or r.Status() != 0 or r.Root() <= x or abs(f.Eval(r.Root())) > 1e-5:
      return 2
    root = r.Root()
    if root > 1:
      root = 1
    return root - x

  def revInterval(x):
    if math.isnan(x): return 2
#    r = Math.BrentRootFinder()
    r = Math.Roots.Bisection()
    f = TF1("intfunc", "TMath::BetaIncomplete([0],[2],[3]) - TMath::BetaIncomplete(x,[2],[3]) - [1]", 0.01, x)
    f.SetParameter(0, x)
    f.SetParameter(1, conf)
    f.SetParameter(2, result + 1)
    f.SetParameter(3, trials - result + 1)
    w = Math.WrappedTF1(f)
    r.SetFunction(w, -0.01, x)
    maxtries = 3
    while maxtries:
      if not r.Solve() or r.Status() != 0 or r.Root() >= x or abs(f.Eval(r.Root())) > 1e-4:
        maxtries -= 1
        if not maxtries:
          return 2
      else:
        break
    root = r.Root()
    if root < 0:
      root = 0
    return x - root

  if trials < result: #stupid negative weights
    return Uncertainty(1, (1-trials/result, 0))
    

  centre = result/float(trials)
  mine = 0
  mini = 0
  if result == 0:
    mini = interval(0)
    return Uncertainty(centre, (0, mini))
  elif result == trials:
    mini = revInterval(1.)
    return Uncertainty(centre, (mini, 0))
  elif not bays:
    de = 1.0/float(trials)*math.sqrt(result*(1-centre))
    return Uncertainty(centre, de)
  else:
    de = 1.0/float(trials)*math.sqrt(result*(1-centre))
    bestguess = centre - de
    minimiser = TMinuit(1)
    minimiser.SetPrintLevel(-1)
    def fcn(npar, gin, f, par, iflag):
      f[0] = interval(par[0])
    minimiser.SetFCN(fcn)
    minimiser.DefineParameter(0, 'mineff', bestguess, de/10, 0, 1)
    minimiser.Migrad()
    xval = array('d', [0])
    xerr = array('d', [0])
    minimiser.GetParameter(0,xval,xerr)

    mine = xval[0]
    mini = interval(mine)
    return Uncertainty(centre, (centre - mine, mini+mine-centre))

def propagateAnyMC(function, *args, **kwargs):
  results = []
  samples = 1000
  if 'samples' in kwargs:
    samples = kwargs['samples']

  conf = 0.68
  if 'conf' in kwargs:
    conf = kwargs['conf']

  for s in xrange(samples):
    params = []
    for arg in args:
      params.append(arg.sample())
    results.append(function(*params))
  results.sort()
  val = results[int(0.5*samples)]
  low = results[int(0.5*(1-conf)*samples)] - val
  high = val - results[int(0.5*(1+conf)*samples)]
  return Uncertainty(val, (low, high))


#def propagateAddBasic(a, b):
#  if len(a) == 2
