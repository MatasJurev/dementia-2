from asyncio import TimeoutError, CancelledError
import discord
from discord.ext import commands
import random

game_started = False
bot = None

# Tic Tac Toe board
board = ['⬜', '⬜', '⬜',
         '⬜', '⬜', '⬜',
         '⬜', '⬜', '⬜']

numbers = [i for i in '1️⃣  2️⃣  3️⃣  4️⃣  5️⃣  6️⃣  7️⃣  8️⃣  9️⃣ '.split(' ') if i]

def init_tictactoe(bot_instance):
    global bot
    bot = bot_instance

def display_board():
    return f"{board[0]} {board[1]} {board[2]}\n" \
           f"{board[3]} {board[4]} {board[5]}\n" \
           f"{board[6]} {board[7]} {board[8]}"

def check_winner(symbol):
    # Check rows, columns, and diagonals
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] == symbol:
            return True
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == symbol:
            return True
    if board[0] == board[4] == board[8] == symbol or board[2] == board[4] == board[6] == symbol:
        return True
    return False

def is_board_full():
    return '⬜' not in board

def reset_game():
    global board
    board = ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']

# Command to play against the bot or another user
@commands.command(name='toe')
async def tic_tac_toe(ctx, opponent: discord.User = None):
    global game_started
    if game_started:
        await ctx.send("A game is already in progress.")
        return

    if opponent:
        # Play against another user
        if opponent.id == ctx.author.id:
            await ctx.send("You can't play against yourself!")
            return
        await ctx.send(f"{opponent.mention}, {ctx.author.mention} has challenged you to a game of Tic Tac Toe!\n"
                       "React with ✅ to accept or ❌ to decline.")
        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: u == opponent and r.emoji in ['✅', '❌'])
        except TimeoutError:
            await ctx.send(f"{opponent.mention} did not respond. The challenge has been declined.")
            return
        if reaction.emoji == '❌':
            await ctx.send(f"{opponent.mention} has declined the challenge.")
            return
    else:
        # Play against the bot
        await ctx.send(f"{ctx.author.mention}, you are playing against the bot.")

    game_started = True
    reset_game()
    turn = random.choice([ctx.author, opponent]) if opponent else ctx.author

    # Display the initial state of the board
    message = await ctx.send(f"{turn.mention}'s turn\n{display_board()}")

    while 1:
        #clear reactions
        for number in numbers:
            await message.remove_reaction(number, bot.user)
            await message.remove_reaction(number, ctx.author)
            await message.remove_reaction(number, opponent) if opponent else None

        # Add reactions for the user to make a move
        for number in numbers:
            await message.add_reaction(number)

        # Wait for the player's move
        def check_reaction(reaction, user):
            return user == turn and str(reaction.emoji) in numbers

        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
        except (TimeoutError, CancelledError):
            await ctx.send(f"{turn.mention} took too long to make a move. The game has ended.")
            return

        # Update the board with the player's move
        move = numbers.index(str(reaction.emoji))

        if board[move] != '⬜':
            await ctx.send("That spot is already taken. Try again.")
            continue

        board[move] = '❌' if turn == ctx.author else '⭕'

        # Check if the current player has won
        if check_winner('❌' if turn == ctx.author else '⭕'):
            await message.edit(content=f"{turn.mention} wins!\n{display_board()}")
            break

        # Check if the board is full (draw)
        if is_board_full():
            await message.edit(content=f"It's a draw!\n{display_board()}")
            break

        # Switch turns
        turn = ctx.author if turn == opponent else opponent

        if turn is None: #bot's turn
            move = get_ai_move()
            board[move] = '⭕'
            turn = ctx.author

        # Update the message with the new board state
        await message.edit(content=f"{turn.mention}'s turn\n{display_board()}")

    reset_game()
    game_started = False

def minimax(new_board, player):
    avail_spots = [i for i in range(len(new_board)) if new_board[i] == '⬜']

    # Base cases: check for a terminal state
    if check_winner('❌'):
        return {'score': -10}
    elif check_winner('⭕'):
        return {'score': 10}
    elif len(avail_spots) == 0:
        return {'score': 0}

    moves = []

    # Loop through available spots
    for i in avail_spots:
        move = {}
        move['index'] = i
        new_board[i] = player

        # Recursively simulate the next move
        if player == '⭕':
            result = minimax(new_board, '❌')
            move['score'] = result['score']
        else:
            result = minimax(new_board, '⭕')
            move['score'] = result['score']

        # Reset the spot to empty after simulation
        new_board[i] = '⬜'
        moves.append(move)

    # Determine the best move
    if player == '⭕':
        best_move = max(moves, key=lambda x: x['score'])  # Maximize score for AI
    else:
        best_move = min(moves, key=lambda x: x['score'])  # Minimize score for player

    return best_move


def get_ai_move():
    return minimax(board[:], '⭕')['index']
