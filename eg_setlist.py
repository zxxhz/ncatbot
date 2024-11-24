@bot_client.message(['private'])
async def reply_private(message: PrivateMessage):
    print(message)
    if message.raw_message == "hi":
        """1. 设置昵称 2. 点赞 3. 设置个性签名 4. 设置头像"""
        # 1. await bot.set_qq_profile(nickname="Ncatbot", personal_note="这是一个测试~", sex="male")
        # 2. await bot.send_like(user_id=message.user_id, times=5)
        # 3. await bot.set_qq_profile(longNick="你好")
        await bot.set_qq_profile(avatar="avatar.png")