"""
Inspirational Quotes System for RedScraperPro
🩸 Stoic, Kafka, Dostoevsky, and Itachi Uchiha Themed Quotes 🩸
"""

import random
import json
from pathlib import Path
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align


class Quotes:
    """Manages and displays inspirational quotes"""
    
    def __init__(self):
        self.console = Console()
        
        # Stoic Quotes
        self.stoic_quotes = [
            "\"You have power over your mind - not outside events. Realize this, and you will find strength.\" - Marcus Aurelius",
            "\"The happiness of your life depends upon the quality of your thoughts.\" - Marcus Aurelius",
            "\"Waste no more time arguing what a good man should be. Be one.\" - Marcus Aurelius",
            "\"It is not what happens to you, but how you react to it that matters.\" - Epictetus",
            "\"No one can hurt you without your permission.\" - Eleanor Roosevelt",
            "\"The best revenge is not to be like your enemy.\" - Marcus Aurelius",
            "\"You are an actor in a play, which is as the author wants it to be.\" - Epictetus",
            "\"The only true wisdom is in knowing you know nothing.\" - Socrates",
            "\"Difficulties strengthen the mind, as labor does the body.\" - Seneca",
            "\"Every new beginning comes from some other beginning's end.\" - Seneca",
            "\"We suffer more often in imagination than in reality.\" - Seneca",
            "\"The willing, destiny guides them. The unwilling, destiny drags them.\" - Seneca",
            "\"Man is disturbed not by things, but by the views he takes of things.\" - Epictetus",
            "\"The mind that is not baffled is not employed.\" - Wendell Berry",
            "\"Accept the things to which fate binds you, and love the people with whom fate brings you together.\" - Marcus Aurelius"
        ]
        
        # Kafka Quotes
        self.kafka_quotes = [
            "\"I am a cage, in search of a bird.\" - Franz Kafka",
            "\"A book must be the axe for the frozen sea inside us.\" - Franz Kafka",
            "\"Don't bend; don't water it down; don't try to make it logical; don't edit your own soul according to the fashion.\" - Franz Kafka",
            "\"I am free and that is why I am lost.\" - Franz Kafka",
            "\"The meaning of life is that it stops.\" - Franz Kafka",
            "\"A non-writing writer is a monster courting insanity.\" - Franz Kafka",
            "\"Better to have, and not need, than to need, and not have.\" - Franz Kafka",
            "\"Every revolution evaporates and leaves behind only the slime of a new bureaucracy.\" - Franz Kafka",
            "\"In the struggle between yourself and the world, second the world.\" - Franz Kafka",
            "\"The truth will set you free, but first it will piss you off.\" - Franz Kafka",
            "\"There are only two things. Truth and lies. Truth is indivisible, hence it cannot recognize itself.\" - Franz Kafka",
            "\"We are sinful not only because we have eaten of the Tree of Knowledge, but also because we have not yet eaten of the Tree of Life.\" - Franz Kafka",
            "\"What is love? After all, it is quite simple. Love is everything which enhances, widens, and enriches our life.\" - Franz Kafka",
            "\"Youth is happy because it has the capacity to see beauty.\" - Franz Kafka",
            "\"The chains of tormented mankind are made out of red tape.\" - Franz Kafka"
        ]
        
        # Dostoevsky Quotes
        self.dostoevsky_quotes = [
            "\"The mystery of human existence lies not in just staying alive, but in finding something to live for.\" - Fyodor Dostoevsky",
            "\"Pain and suffering are always inevitable for a large intelligence and a deep heart.\" - Fyodor Dostoevsky",
            "\"The soul is healed by being with children.\" - Fyodor Dostoevsky",
            "\"Above all, don't lie to yourself.\" - Fyodor Dostoevsky",
            "\"To love someone means to see them as God intended them.\" - Fyodor Dostoevsky",
            "\"We sometimes encounter people, even perfect strangers, who begin to interest us at first sight.\" - Fyodor Dostoevsky",
            "\"The degree of civilization in a society can be judged by entering its prisons.\" - Fyodor Dostoevsky",
            "\"If you want to overcome the whole world, overcome yourself.\" - Fyodor Dostoevsky",
            "\"Man is sometimes extraordinarily, passionately, in love with suffering.\" - Fyodor Dostoevsky",
            "\"The cleverest of all, in my opinion, is the man who calls himself a fool at least once a month.\" - Fyodor Dostoevsky",
            "\"Beauty will save the world.\" - Fyodor Dostoevsky",
            "\"Can you have despair without hope?\" - Fyodor Dostoevsky",
            "\"Compassion is the most important, perhaps the sole law of human existence.\" - Fyodor Dostoevsky",
            "\"Don't let us forget that the causes of human actions are usually immeasurably more complex than our subsequent explanations of them.\" - Fyodor Dostoevsky",
            "\"Realists do not fear the results of their study.\" - Fyodor Dostoevsky"
        ]
        
        # Itachi Uchiha Themed Quotes (Philosophical/Dark)
        self.itachi_quotes = [
            "\"Those who cannot acknowledge themselves will eventually fail.\" - Itachi Uchiha",
            "\"People's lives don't end when they die. It ends when they lose faith.\" - Itachi Uchiha",
            "\"Knowledge and awareness are vague, and perhaps better called illusions.\" - Itachi Uchiha",
            "\"Self-sacrifice... A nameless shinobi who protects peace within its shadow.\" - Itachi Uchiha",
            "\"The village does have its dark side and its inconsistencies, but I'm still Konoha's Itachi Uchiha.\" - Itachi Uchiha",
            "\"You focus on the trivial, and lose sight of what is most important.\" - Itachi Uchiha",
            "\"It is not the face that makes someone a monster, it is the choices they make with their lives.\" - Itachi Uchiha",
            "\"Those who forgive themselves, and are able to accept their true nature... They are the strong ones.\" - Itachi Uchiha",
            "\"Even the strongest of opponents always has a weakness.\" - Itachi Uchiha",
            "\"The ones who aren't able to acknowledge their own selves are bound to fail.\" - Itachi Uchiha",
            "\"True change cannot be made if it is bound by laws and limitations, predictions and imagination.\" - Itachi Uchiha",
            "\"We do not know what kind of people we truly are until the moment before our deaths.\" - Itachi Uchiha",
            "\"Reality is the harshest thing there is.\" - Itachi Uchiha",
            "\"No single thing is perfect by itself. That's why we're born to attract other things to make up for what we lack.\" - Itachi Uchiha",
            "\"The moment people come to know love, they run the risk of carrying hate.\" - Itachi Uchiha"
        ]
        
        # Additional philosophical quotes
        self.philosophical_quotes = [
            "\"In the midst of winter, I found there was, within me, an invincible summer.\" - Albert Camus",
            "\"The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.\" - Albert Camus",
            "\"There is but one truly serious philosophical problem, and that is suicide.\" - Albert Camus",
            "\"Man is condemned to be free; because once thrown into the world, he is responsible for everything he does.\" - Jean-Paul Sartre",
            "\"Hell is other people.\" - Jean-Paul Sartre",
            "\"The unexamined life is not worth living.\" - Socrates",
            "\"I think, therefore I am.\" - René Descartes",
            "\"God is dead. God remains dead. And we have killed him.\" - Friedrich Nietzsche",
            "\"What does not kill me, makes me stronger.\" - Friedrich Nietzsche",
            "\"In every real man a child is hidden that wants to play.\" - Friedrich Nietzsche",
            "\"The individual has always had to struggle not to be overwhelmed by the tribe.\" - Friedrich Nietzsche",
            "\"Whoever fights monsters should see to it that in the process he does not become a monster.\" - Friedrich Nietzsche",
            "\"And if you gaze long into an abyss, the abyss also gazes into you.\" - Friedrich Nietzsche",
            "\"Without music, life would be a mistake.\" - Friedrich Nietzsche",
            "\"That which is done out of love always takes place beyond good and evil.\" - Friedrich Nietzsche"
        ]
        
        # Combine all quotes
        self.all_quotes = (
            self.stoic_quotes + 
            self.kafka_quotes + 
            self.dostoevsky_quotes + 
            self.itachi_quotes + 
            self.philosophical_quotes
        )
    
    def get_random_quote(self, category="all"):
        """Get a random quote from specified category"""
        if category == "stoic":
            return random.choice(self.stoic_quotes)
        elif category == "kafka":
            return random.choice(self.kafka_quotes)
        elif category == "dostoevsky":
            return random.choice(self.dostoevsky_quotes)
        elif category == "itachi":
            return random.choice(self.itachi_quotes)
        elif category == "philosophical":
            return random.choice(self.philosophical_quotes)
        else:
            return random.choice(self.all_quotes)
    
    def display_random_quote(self, category="all", style="panel"):
        """Display a random quote with styling"""
        quote = self.get_random_quote(category)
        
        if style == "panel":
            quote_panel = Panel(
                f"[italic dim white]{quote}[/italic dim white]",
                title="[bold red]💭 Wisdom for Your Journey[/bold red]",
                border_style="red",
                padding=(1, 2)
            )
            self.console.print(quote_panel)
        elif style == "simple":
            quote_text = Text(f"💭 {quote}", style="italic dim white")
            self.console.print(quote_text)
        elif style == "centered":
            quote_text = Text(quote, style="italic dim white")
            self.console.print(Align.center(quote_text))
    
    def display_startup_quote(self):
        """Display a special quote for startup"""
        startup_quotes = [
            "\"In the darkness of data, we find the light of knowledge.\" - RedScraperPro Philosophy",
            "\"Every dataset tells a story, but not every story is worth telling.\" - Data Wisdom",
            "\"The art of scraping is not in taking everything, but in knowing what to take.\" - Digital Philosophy",
            "\"Information is power, but wisdom is knowing how to use it.\" - Modern Stoicism",
            "\"In the realm of data, we are all archaeologists of the digital age.\" - Cyber Philosophy"
        ]
        
        quote = random.choice(startup_quotes)
        quote_text = Text(f"💭 {quote}", style="italic bold red")
        self.console.print(Align.center(quote_text))
        self.console.print()
    
    def display_completion_quote(self):
        """Display a quote upon completion"""
        completion_quotes = [
            "\"The journey of a thousand miles begins with a single step.\" - Lao Tzu",
            "\"What we plant in the soil of contemplation, we shall reap in the harvest of action.\" - Meister Eckhart",
            "\"The best time to plant a tree was 20 years ago. The second best time is now.\" - Chinese Proverb",
            "\"Success is not final, failure is not fatal: it is the courage to continue that counts.\" - Winston Churchill",
            "\"The only impossible journey is the one you never begin.\" - Tony Robbins"
        ]
        
        quote = random.choice(completion_quotes)
        quote_panel = Panel(
            f"[italic green]{quote}[/italic green]",
            title="[bold green]🎯 Journey Complete[/bold green]",
            border_style="green"
        )
        self.console.print(quote_panel)
    
    def display_error_quote(self):
        """Display a quote for error situations"""
        error_quotes = [
            "\"Failure is simply the opportunity to begin again, this time more intelligently.\" - Henry Ford",
            "\"The only real mistake is the one from which we learn nothing.\" - Henry Ford",
            "\"Every adversity, every failure, every heartache carries with it the seed of an equal or greater benefit.\" - Napoleon Hill",
            "\"It is impossible to live without failing at something, unless you live so cautiously that you might as well not have lived at all.\" - J.K. Rowling",
            "\"Success is stumbling from failure to failure with no loss of enthusiasm.\" - Winston Churchill"
        ]
        
        quote = random.choice(error_quotes)
        quote_text = Text(f"💭 {quote}", style="italic yellow")
        self.console.print(quote_text)
    
    def save_quotes_to_file(self, filename="quotes_database.json"):
        """Save all quotes to a JSON file"""
        quotes_data = {
            "stoic": self.stoic_quotes,
            "kafka": self.kafka_quotes,
            "dostoevsky": self.dostoevsky_quotes,
            "itachi": self.itachi_quotes,
            "philosophical": self.philosophical_quotes
        }
        
        filepath = Path("assets") / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(quotes_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_quotes_from_file(self, filename="quotes_database.json"):
        """Load quotes from a JSON file"""
        filepath = Path("assets") / filename
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                quotes_data = json.load(f)
                
                self.stoic_quotes = quotes_data.get("stoic", self.stoic_quotes)
                self.kafka_quotes = quotes_data.get("kafka", self.kafka_quotes)
                self.dostoevsky_quotes = quotes_data.get("dostoevsky", self.dostoevsky_quotes)
                self.itachi_quotes = quotes_data.get("itachi", self.itachi_quotes)
                self.philosophical_quotes = quotes_data.get("philosophical", self.philosophical_quotes)
                
                # Update combined quotes
                self.all_quotes = (
                    self.stoic_quotes + 
                    self.kafka_quotes + 
                    self.dostoevsky_quotes + 
                    self.itachi_quotes + 
                    self.philosophical_quotes
                )
                
                return True
        return False
