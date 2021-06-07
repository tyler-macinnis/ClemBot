import datetime
import typing as t
from dataclasses import dataclass

from dataclasses_json import LetterCase, DataClassJsonMixin, dataclass_json

from bot.api.api_client import ApiClient
from bot.api.base_route import BaseRoute
from bot.consts import Infractions


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Infraction(DataClassJsonMixin):
    id: int
    guild_id: int
    author_id: int
    subject_id: int
    type: str
    reason: str
    duration: int
    time: str
    active: int


class ModerationRoute(BaseRoute):

    def __init__(self, api_client: ApiClient):
        super().__init__(api_client)

    async def insert_ban(self, *,
                         guild_id: int,
                         author_id: int,
                         subject_id: int,
                         reason: str,
                         **kwargs) -> t.Optional[int]:
        json = {
            'GuildId': guild_id,
            'AuthorId': author_id,
            'SubjectId': subject_id,
            'Reason': reason,
            'Type': Infractions.ban
        }

        resp = await self._client.post('infractions', data=json, **kwargs)

        if resp.status != 200:
            return None

        return resp.value['infractionId']

    async def insert_mute(self, *,
                          guild_id: int,
                          author_id: int,
                          subject_id: int,
                          reason: t.Optional[str] = None,
                          duration: datetime,
                          **kwargs) -> t.Optional[int]:
        json = {
            'GuildId': guild_id,
            'AuthorId': author_id,
            'SubjectId': subject_id,
            'Reason': reason,
            'Duration': duration,
            'Type': Infractions.mute,
            'Active': True
        }

        resp = await self._client.post('infractions', data=json, **kwargs)

        if resp.status != 200:
            return None

        return resp.value['infractionId']

    async def insert_warn(self, *,
                          guild_id: int,
                          author_id: int,
                          subject_id: int,
                          reason: str,
                          **kwargs) -> t.Optional[int]:
        json = {
            'GuildId': guild_id,
            'AuthorId': author_id,
            'SubjectId': subject_id,
            'Reason': reason,
            'Type': Infractions.warn
        }
        resp = await self._client.post('infractions', data=json, **kwargs)

        if resp.status != 200:
            return None

        return resp.value['infractionId']

    async def delete_infraction(self, infraction_id: int, **kwargs) -> int:
        resp = await self._client.delete(f'infractions/{infraction_id}', **kwargs)
        return resp.value

    async def deactivate_mute(self, infraction_id: int, **kwargs) -> int:
        resp = await self._client.patch(f'infractions/{infraction_id}/deactivate', **kwargs)

        if resp.status != 200:
            return None

        return resp.value

    async def get_infraction(self, infraction_id: int) -> t.Optional[Infraction]:
        resp = await self._client.get(f'infractions/{infraction_id}')

        if resp.status != 200:
            return None

        return resp.value

    async def get_guild_infractions(self, guild_id: int) -> t.Optional[t.Iterator[Infraction]]:
        resp = await self._client.get(f'guilds/{guild_id}/infractions')

        if resp.status != 200:
            return None

        return [Infraction.from_dict(i) for i in resp.value]

    async def get_guild_infractions_user(self, guild_id: int, user_id: int) -> t.Optional[t.Iterator[Infraction]]:
        resp = await self._client.get(f'users/infractions/{user_id}/{guild_id}')

        if resp.status != 200:
            return None

        return [Infraction.from_dict(i) for i in resp.value]

    async def get_guild_warns_user(self, guild_id: int, user_id: int) -> t.Optional[t.Iterator[Infraction]]:
        resp = await self._client.get(f'users/infractions/{user_id}/{guild_id}/warn')

        if resp.status != 200:
            return None

        return [Infraction.from_dict(i) for i in resp.value]

    async def get_guild_mutes_user(self, guild_id: int, user_id: int) -> t.Optional[t.Iterator[Infraction]]:
        resp = await self._client.get(f'users/infractions/{user_id}/{guild_id}/mute')

        if resp.status != 200:
            return None

        return [Infraction.from_dict(i) for i in resp.value]

    async def get_guild_bans_user(self, guild_id: int, user_id: int) -> t.Optional[t.Iterator[Infraction]]:
        resp = await self._client.get(f'users/infractions/{user_id}/{guild_id}/ban')

        if resp.status != 200:
            return None

        return [Infraction.from_dict(i) for i in resp.value]
