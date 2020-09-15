from PIL import Image
from IPython import display as disp
from io import BytesIO
import heapq

def show(im):
  b = BytesIO()
  im.save(b, format='png')
  disp.display(disp.Image(data=b.getvalue(), format='png', embed=True))

darkmaze = Image.open('darkmaze.jpg')
#show(darkmaze)
im = darkmaze.convert('L').point(lambda x: 0 if x < 200 else 1, '1')

begin = (402, 984)
end = (398, 24)

top, right, bottom, left = 22, 793, 986, 7

def dark(p):
  def inner():
    for ox in range(-3, 4):
      for oy in range(-3, 4):
        x, y = p
        yield darkmaze.getpixel((x + ox, y + oy)) == (0, 0, 0)
  return max(inner())

def cost(p):
  return 1000 if dark(p) else 1

def forbidden(p):
  x, y = p
  return x < left or y < top or x > right or y > bottom or im.getpixel(p) == 0

heap = []

heapq.heappush(heap, (0, begin))

closed = {}
d = {begin : 0}
prev = {}

while heap:
  value, p = heapq.heappop(heap)
  x, y = p
  if p == end:
    break
  if p in closed:
    continue
  #print p
  closed[p] = 1
  for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
    target = (x + dx, y + dy)
    if not forbidden(target) and target not in closed:
      if d[p] + cost(target) < d.get(target, float('inf')):
        d[target] = d[p] + cost(target)
        heapq.heappush(heap, (d[target], target))
        prev[target] = p

path = []

p = end
path.append(p)
while p != begin:
  p = prev[p]
  path.append(p)

out = darkmaze.point(lambda p: p / 2).convert('RGB')
for p in path:
  out.putpixel(p, (255, 255, 255))
#out.save('out.png', format='png')
show(out)
