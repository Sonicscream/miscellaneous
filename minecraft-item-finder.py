import nbt

BLACKLIST = [
	"minecraft:kelp",
	"minecraft:rail",
	"minecraft:lily_pad"
]

def outputItems(path, data):
	f = open(path, "w")
	f.write(str(items))
	f.close()

def debugMessage(string):
	print(string)
	pass

def entityToStr(entity):
	pos = entity['Pos']
	
	x = float(str(pos[0]))
	y = float(str(pos[1]))
	z = float(str(pos[2]))

	if str(entity['Item']['id']) in BLACKLIST:
		raise

	# If this fails it is because its not a dropped item.
	id = f"{entity['Item']['Count']}x {entity['Item']['id']}"
	
	return f"{id}\t{[x,y,z]}"

def chunkToStr(chunk):
	global items
	s = ""
	if len(chunk['Level']['Entities']) > 0:
		s += str(len(chunk['Level']['Entities']))
	for entity in chunk['Level']['Entities']:
		#if entity['id'] == "minecraft:item":
		try:
			items += entityToStr(entity) + "\n"
		except:
			pass
	return s	

try:
	ax = -10000
	ay = -10000
	bx = 10000
	by = 10000

	path = 'yourWorldFolderPath/'
	
	rax = ax // 512
	rbx = bx // 512
	ray = ay // 512
	rby = by // 512
	
	regions = []
	chunks = []
	items = ""
	regionsCounter = 0
	chunksCounter = 0
	itemsCounter = 0
	
	for x in range(rax, rbx + 1, 1):
		for y in range(ray, rby + 1, 1):
			regions.append([x, y])
	
	for x in range(0, 31 + 1, 1):
		for y in range(0, 31 + 1, 1):
			chunks.append([x, y])
	
	for region in regions:
		rx, ry = region
		r = None
		try:
			r = nbt.region.RegionFile(filename=f'{path}/region/r.{rx}.{ry}.mca')
			for chunk in chunks:
				cx, cy = chunk
				c = None
				try:
					c = r.get_nbt(cx, cy)
					print(f"{region}\t{chunk}  \t:\t{chunkToStr(c)}")
				except nbt.region.InconceivedChunk:
					pass
				#except:
				#	debugMessage(f"{region} {chunk} : Error")
				#	continue
		except FileNotFoundError:
			pass
		#except:
		#	debugMessage(f"{region} [] : Error")
		#	continue

	outputItems(items)
except KeyboardInterrupt:
	outputItems(items)
	quit()
