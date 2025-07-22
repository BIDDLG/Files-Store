from pyrogram import Client
from typing import Any, Optional
from pyrogram.types import Message
from pyrogram.file_id import FileId
from pyrogram.raw.types.messages import Messages
from TechVJ.server.exceptions import FIleNotFound

# ✅ Format file size helper
def format_file_size(size_bytes: int) -> str:
    if size_bytes >= 1024**3:
        return f"{round(size_bytes / 1024**3, 2)} GB"
    elif size_bytes >= 1024**2:
        return f"{round(size_bytes / 1024**2, 2)} MB"
    elif size_bytes >= 1024:
        return f"{round(size_bytes / 1024, 2)} KB"
    return f"{size_bytes} B"

def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media

async def parse_file_id(message: "Message") -> Optional[FileId]:
    media = get_media_from_message(message)
    if media:
        return FileId.decode(media.file_id)

async def parse_file_unique_id(message: "Messages") -> Optional[str]:
    media = get_media_from_message(message)
    if media:
        return media.file_unique_id

async def get_file_ids(client: Client, chat_id: int, id: int) -> Optional[FileId]:
    message = await client.get_messages(chat_id, id)
    if message.empty:
        raise FIleNotFound

    media = get_media_from_message(message)
    file_unique_id = await parse_file_unique_id(message)
    file_id = await parse_file_id(message)

    file_size = getattr(media, "file_size", 0)
    mime_type = getattr(media, "mime_type", "")
    file_name = getattr(media, "file_name", "")

    setattr(file_id, "file_size", file_size)
    setattr(file_id, "mime_type", mime_type)
    setattr(file_id, "file_name", file_name)
    setattr(file_id, "unique_id", file_unique_id)

    # ✅ Set custom formatted details: {file_name} | {size} | {mime}
    detail_string = f"{file_name or 'File'} | {format_file_size(file_size)} | {mime_type or 'unknown'}"
    setattr(file_id, "file_details", detail_string)

    return file_id

def get_hash(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_unique_id", "")[:6]

def get_name(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, 'file_name', "")

def get_media_file_size(m):
    media = get_media_from_message(m)
    return getattr(media, "file_size", 0)
