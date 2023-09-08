#             
#                 _____                             _   _
#     /    '                            /  /|              /
#---/__-------------)__---)__---------/| /-|----__----__-/---__-
#   /        /   /  /   ) /   ) /   / / |/  |  /   ) /   /   (_ `
# _/________(___(__/_____/_____(___/_/__/___|_(___/_(___/___(__)_
#                                /
#                           (_ /
#
#
#
# meta developer: @AstroModules | @FurryMods
# requires: vk_api

from .. import loader, utils
import vk_api
import random

@loader.tds
class VKNow(loader.Module):
    '''Модуль для просмотра проигрываемых треков в VK'''

    strings = {
        'name': 'VKNow',
        'not_token_or_id': (
            '<emoji document_id=5240241223632954241>🚫</emoji> <b>Неверный токен</b>!\n'
            '<emoji document_id=5443038326535759644>💬</emoji> Заполните поле с токеном <a href="{}"><b>по туториалу</b></a>'
        ),
        'no_track': '<emoji document_id=5240241223632954241>🚫</emoji> <b>Никакой трек не играет</b> или <b>закрыт</b> доступ <b>к статусу</b>!',
        'result': (
            '{} <b>Сейчас играет</b>:\n'
            '{} <code>{} - {}</code>'
        )
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                'token',
                None,
                lambda: 'VK_API',
                validator=loader.validators.Hidden()
            ),
            loader.ConfigValue(
                'account',
                None,
                lambda: 'ID или @username вашего аккаунта в VK'
            )
        )

    async def emoji(self):
        one = [
            '<emoji document_id=5451636889717062286>🎧</emoji>', '<emoji document_id=5375203677487248777>🎛️</emoji>',
            '<emoji document_id=5456140674028019486>🎚️</emoji>', '<emoji document_id=5224607267797606837>🔈</emoji>',
            '<emoji document_id=5424972470023104089>🎵</emoji>'
        ]
        two = [
            '<emoji document_id=5460795800101594035>🎤</emoji>', '<emoji document_id=5449816553727998023>🎹</emoji>',
            '<emoji document_id=5361964771509808811>💻</emoji>', '<emoji document_id=5451814216031809603>🎙️</emoji>',
            '<emoji document_id=5416117059207572332>🔎</emoji>'
        ]
        return random.choice(one), random.choice(two)


    async def account_id(self):
        acc_id = self.config['account']
        if f'{acc_id}'.isdigit():
            return int(acc_id)
        else:
            return acc_id

    async def get_now_playing_track(self):
        token = self.config['token']
        account = await self.account_id()
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        res = vk.users.get(user_ids=account, fields="status")[0]
        curr_music = res['status_audio']
        if curr_music:
            author = curr_music['artist']
            title = curr_music['title']
            return author, title
        else:
            return False, False

    @loader.command(alias='vkn')
    async def vknow(self, message):
        '''- посмотреть проигрываемый трек в VK'''
        if (
            self.config['token'] == None 
            or self.config['account'] == None
        ):
            return await utils.answer(message, self.strings('not_token_or_id').format('https://t.me/help_code/18')) 

        author, title = await self.get_now_playing_track()

        if author == False:
            return await utils.answer(message, self.strings('no_track'))

        file = (await message.client.inline_query('vkmusic_bot', f'{author} {title}'))
        text = self.strings('result').format(*(await self.emoji()), author, title)

        try:
            await utils.answer_file(message, file[1].result.document, caption=text, reply_markup=[{'text': 'da', 'url': 'https://pornhub.com'}])
        except:
            await utils.answer(message, text)
