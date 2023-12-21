import string
import requests
import numpy
import logging
from .. import loader, utils

class NitroGenMod(loader.Module):
	'''Модуль для просмотра проигрываемых треков в VK
✨ Идея: @Astroofftop
🎨 Баннер: @FurryMods
⌨️ Код: @toxicuse | @corelv'''
	async def client_ready(self, client, db):
		self.client = client
		self.db = db

	strings = {'name': 'NitroGen'}
	async def main(self, args): 
		num = int(args)
		valid = []
		invalid = 0
		chars = []
		chars[:0] = string.ascii_letters + string.digits
		c = numpy.random.choice(chars, size=[num, 16])
		for s in c:
			code = ''.join(x for x in s)
			url = f"https://discord.gift/{code}"
			result = await self.quickChecker(url)
			if result == False:
				invalid += 1
			else:
				valid.append(url)
				return url
		return False

	async def quickChecker(self, nitro: str):
		url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
		response = requests.get(url) 
		s = (requests.get(url)).json()
		if s['message'] == '404: Not Found':
			return False 
		if s['message'] == 'You are being rate limited.':
			return False 
		else:
			return nitro

	async def gencmd(self, message):
		'''<int> - try generate discord nitro'''
		args = utils.get_args_raw(message)
		msg = await utils.answer(message, (
			'<emoji document_id=5307675706283533118>🫥</emoji>'
			f' <b>Запускаю попытку генерации нитро. Попыток: <code>{args}</code></b>'
		))
		result = await self.main(args)
		if result == False:
			await utils.answer(msg, (
				'<emoji document_id=5274083487161261629>🔴</emoji>'
				' <b>Попытка не увенчалась успехом. Ни одного нитро не было поймано.'
				f'\nПопыток произведено: <code>{args}</code></b>'
			))
		else:
			await utils.answer(msg, (
				'<emoji document_id=5287554789524120325>🔵</emoji> '
				'<b>Пойман халявный дискорд нитро! Вот ссылка на него:</b>'
				f'\n\n{result}'
			))
