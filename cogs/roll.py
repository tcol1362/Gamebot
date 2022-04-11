from discord.ext import commands
import random

# Determines if the value can be converted to an integer
# Parameters: s - input string
# Returns: boolean. True if can be converted, False if it throws an error.
def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Roll die and get a random number between a and b (inclusive) adding/subtracting the modifier
# Parameters: a [low number], b [high number], modifier [amount to add/subtract to total]
# threshold [number that result needs to match or exceed to count as a success]
# Returns: str 
def roll_basic(a, b, modifier, threshold):
    results = ""
    base = random.randint(int(a), int(b))
    if (base + modifier) >= threshold:
        if modifier != 0:
            if modifier > 0:
                results += "***Success***: {}+{} [{}] meets or beats the {} threshold.".format(base, modifier, (base + modifier), threshold)
            else:
                results += "***Success***: {}{} [{}] does not meet the {} threshold.".format(base, modifier, (base + modifier), threshold)
        else:
            results += "***Success***: {}".format(base)
    else:
        if modifier != 0:
            if modifier > 0:
                results += "***Failure***: {}+{} [{}]".format(base, modifier, (base + modifier))
            else:
                results += "***Failure***: {}{} [{}]".format(base, modifier, (base + modifier))
        else:
            results += "***Failure***: {}".format(base)
    return results

# Rolls a set of die and returns either number of hits or the total amount
# Parameters: num_of_dice [Number of dice to roll], dice_type[die type (e.g. d8, d6), 
# hit [number that must be exceeded to count as a success], modifier [amount to add to/subtract from total],
# threshold [number of successes needed to be a win]
# Returns: String with results 
def roll_hit(num_of_dice, dice_type, hit, modifier, threshold):
    results = ""
    total = 0
    for x in range(0, int(num_of_dice)):
        y = random.randint(1, int(dice_type))
        if (int(hit) > 0):
            if (y >= int(hit)):
                results += "**{}** ".format(y)
                total += 1
            else:
                results += "{} ".format(y)
        else:
            results += "{} ".format(y)
            total += y
    total += int(modifier)
    if modifier != 0:
        if modifier > 0:
            results += "+{} = {}".format(modifier, total)
        else:
            results += "{} = {}".format(modifier, total)
    else:
        results += "= {}".format(total)
    if threshold != 0:
        if total >= threshold:
            results += " meets or beats the {} threshold. ***Success***".format(threshold)
        else:
            results += " does not meet the {} threshold. ***Failure***".format(threshold)
    return results


class roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Error Detection
    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex):
        print(ex)
        await ctx.send("An issue has occurred with this command. Please contact your administrator for this bot.")

    # !roll_help command to display description
    @commands.command(brief=': command list of "roll" commands')
    async def roll_help(self,ctx):
        await ctx.send('Examples of the "roll" command:\n100  Rolls 1-100.\n50-100  Rolls 50-100.\n3d6  Rolls 3 d6 dice and returns total.\nModifiers:\n! Hit success. 3d6!5 Counts number of rolls that are greater than 5.\nmod: Modifier. 3d6mod3 or 3d6mod-3. Adds 3 to the result.\n \> Threshold. 100>30 returns success if roll is greater than or equal to 30.\n\nFormatting:\nMust be done in order.\nSingle die roll: 1-100mod2>30\nMultiple: 5d6!4mod-2>2')

    # Parse !roll verbiage
    @commands.command(pass_context=True, brief=': dice roll command.\n For full list of dice commands, try "roll_help".')
    async def roll(self, ctx, roll : str):
        a, b, modifier, hit, num_of_dice, threshold, dice_type = 0, 0, 0, 0, 0, 0, 0
        # author: Writer of discord message
        author = ctx.message.author
        if (roll.find('>') != -1):
            roll, threshold = roll.split('>')
        if (roll.find('mod') != -1):
            roll, modifier = roll.split('mod')
        if (roll.find('!') != -1):
            roll, hit = roll.split('!')
        if (roll.find('d') != -1):
            num_of_dice, dice_type = roll.split('d')
        elif (roll.find('-') != -1):
            a, b = roll.split('-')
        else:
            a = 1
            b = roll
        #Validate data
        try:
            if (modifier != 0):
                if (is_num(modifier) is False):
                    raise ValueError("Modifier value format error. Proper usage 1d4+1")
                    return
                else:
                    modifier = int(modifier)
            if (hit != 0):
                if (is_num(hit) is False):
                    raise ValueError("Hit value format error. Proper usage 3d6!5")
                    return
                else:
                    hit = int(hit)
            if (num_of_dice != 0):
                if (is_num(num_of_dice) is False):
                    raise ValueError("Number of dice format error. Proper usage 3d6")
                    return
                else:
                    num_of_dice = int(num_of_dice)
            if (num_of_dice > 200):
                raise ValueError("Too many dice. Please limit to 200 or less.")
                return
            if (dice_type != 0):
                if (is_num(dice_type) is False):
                    raise ValueError("Dice type format error. Proper usage 3d6")
                    return
                else:
                    dice_type = int(dice_type)
            if (a != 0):
                if (is_num(a) is False):
                    raise ValueError("Error: Minimum must be a number. Proper usage 1-50.")
                    return
                else:
                    a = int(a)
            if (b != 0):
                if (is_num(b) is False):
                    raise ValueError("Error: Maximum must be a number. Proper usage 1-50 or 50.")
                    return
                else:
                    b = int(b)
            if (threshold != 0):
                if (is_num(threshold) is False):
                    raise ValueError("Error: Threshold must be a number. Proper usage 1-100>30")
                    return
                else:
                    threshold = int(threshold)
            if (dice_type != 0 and hit != 0):
                if (hit > dice_type):
                    raise ValueError("Error: Hit value cannot be greater than dice type")
                    return
                elif (dice_type < 0):
                    raise ValueError("Dice type cannot be a negative number.")
                    return
                elif (num_of_dice < 0):
                    raise ValueError("Number of dice cannot be a negative number.")
                    return
            if a != 0 and b != 0:
                await ctx.send("{} rolls {}-{}. Result: {}".format(author, a, b, roll_basic(a, b, modifier, threshold)))
            else:
                await ctx.send("{} rolls {}d{}. Results: {}".format(author, num_of_dice, dice_type, roll_hit(num_of_dice, dice_type, hit, modifier, threshold)))
        except ValueError as err:
            # Display error message to channel
            await ctx.send(err)

def setup(bot):
    bot.add_cog(roll(bot))