TOKEN = "8935997239:AAF8bgGYzXz01NgxUb-0Ebfgdy4pRIyJmVI"

questions = [
    # Present Simple
    {"question": "She ___ to school every day.", "options": ["go", "goes", "going", "gone"], "correct": 1},
    {"question": "They ___ football every weekend.", "options": ["play", "plays", "playing", "played"], "correct": 0},

    # Present Continuous
    {"question": "I ___ a book now.", "options": ["read", "reads", "am reading", "readed"], "correct": 2},
    {"question": "Look! He ___ TV.", "options": ["watch", "watches", "is watching", "watched"], "correct": 2},

    # Past Simple
    {"question": "We ___ to Tashkent yesterday.", "options": ["go", "went", "gone", "going"], "correct": 1},
    {"question": "She ___ a letter last night.", "options": ["write", "writes", "wrote", "writing"], "correct": 2},

    # Past Continuous
    {"question": "I ___ sleeping when you called.", "options": ["was", "were", "is", "are"], "correct": 0},
    {"question": "They ___ playing football at 5pm.", "options": ["was", "were", "are", "is"], "correct": 1},

    # Present Perfect
    {"question": "I ___ finished my homework.", "options": ["has", "have", "had", "having"], "correct": 1},
    {"question": "She ___ seen this movie.", "options": ["have", "has", "had", "having"], "correct": 1},

    # Past Perfect
    {"question": "He ___ left before I arrived.", "options": ["had", "has", "have", "having"], "correct": 0},
    {"question": "They ___ finished work when I came.", "options": ["had", "has", "have", "having"], "correct": 0},

    # Future Simple
    {"question": "I ___ call you tomorrow.", "options": ["will", "was", "is", "are"], "correct": 0},
    {"question": "She ___ go to London next year.", "options": ["will", "was", "is", "are"], "correct": 0},

    # Future Continuous
    {"question": "I ___ be working at 5pm.", "options": ["will", "was", "am", "is"], "correct": 0},
    {"question": "They ___ be traveling tomorrow.", "options": ["will", "was", "is", "are"], "correct": 0},

    # Modal Verbs
    {"question": "You ___ study harder.", "options": ["must", "can", "may", "could"], "correct": 0},
    {"question": "He ___ swim very well.", "options": ["can", "must", "should", "would"], "correct": 0},

    # Mixed
    {"question": "She ___ already eaten.", "options": ["has", "have", "had", "having"], "correct": 0},
    {"question": "They ___ playing now.", "options": ["is", "are", "was", "be"], "correct": 1},
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {"index": 0, "score": 0}
    await update.message.reply_text("👋 Welcome!\nUse /quiz to start test.")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"index": 0, "score": 0}
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    idx = user_data[user_id]["index"]

    if idx >= len(questions):
        score = user_data[user_id]["score"]
        await update.message.reply_text(f"🏁 Finished!\nScore: {score}/{len(questions)}")
        return

    q = questions[idx]

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=str(i))]
        for i, opt in enumerate(q["options"])
    ]

    await update.message.reply_text(
        f"❓ Q{idx+1}: {q['question']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    idx = user_data[user_id]["index"]
    q = questions[idx]

    if int(query.data) == q["correct"]:
        user_data[user_id]["score"] += 1
        text = "✅ Correct!"
    else:
        text = f"❌ Wrong! Correct: {q['options'][q['correct']]}"

    user_data[user_id]["index"] += 1

    await query.edit_message_text(text)

    if user_data[user_id]["index"] < len(questions):
        await send_next(query, context)
    else:
        score = user_data[user_id]["score"]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🏁 Quiz finished!\nScore: {score}/{len(questions)}"
        )

async def send_next(query, context):
    user_id = query.from_user.id
    idx = user_data[user_id]["index"]
    q = questions[idx]

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=str(i))]
        for i, opt in enumerate(q["options"])
    ]

    await context.bot.send_message(
        chat_id=user_id,
        text=f"❓ Q{idx+1}: {q['question']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
