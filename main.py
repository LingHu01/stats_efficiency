import tkinter as tk
from tkinter import ttk

def main():
	# create the main window
	root = tk.Tk()
	root.title("stats calculator")
	root.geometry("1600x900")
	root.columnconfigure(0, weight=1)
	root.resizable(False, False)
	root.configure(background= '#2b2b2b')

	#style
	style = ttk.Style()
	style.theme_use('clam')
	style.configure('dark_frame', background= '#2b2b2b')
	style.layout('dark_frame', [('dark_frame', {'sticky': 'nswe'})])
	style.configure('TProgressbar', foreground='#2b2b2b', background='#4b74a4')

	# atk
	atk_frame = ttk.Frame(root, style = 'dark_frame')
	atk_frame.grid(row = 0, pady=(20,5), padx=(80,5), columnspan=2, sticky='w')
	atk = Atk(atk_frame, 70)

	# e_atk
	e_atk_frame = ttk.Frame(root, style = 'dark_frame')
	e_atk_frame.grid(row= 2, pady=(5, 10), padx=(80,0), columnspan=2, sticky='w')
	e_atk = ElementAtk(e_atk_frame, 17)

	# crit
	crit_frame = ttk.Frame(root, style = 'dark_frame')
	crit_frame.grid(row=4, pady=20, padx=(80,0), columnspan=2, sticky='w')
	crit = Crit(crit_frame, 10, 10)

	# di
	ep_frame = ttk.Frame(root, style = 'dark_frame')
	ep_frame.grid(row=8, pady=20, padx=(80, 0), columnspan=2, sticky='w')
	di = DefIgn(ep_frame, 100)

	# ep
	ep_frame = ttk.Frame(root, style = 'dark_frame')
	ep_frame.grid(row=11, pady=20, padx=(80, 0), columnspan=2, sticky='w')
	di = Ep(ep_frame, 100)

	# skill
	skill_frame = ttk.Frame(root, style = 'dark_frame')
	skill_frame.grid(row=13, pady=(10, 0), padx=(80,0), columnspan=2, sticky='w')
	skill = BinaryStats(skill_frame, 0, 0, 'skill %')

	# basic
	basic_frame = ttk.Frame(root, style = 'dark_frame')
	basic_frame.grid(row=14, padx=(80, 0), columnspan=2, sticky='w')
	basic = BinaryStats(basic_frame, 0, 0, 'basic ATK %')

	# Boss DMG
	boss_DMG_frame = ttk.Frame(root, style = 'dark_frame')
	boss_DMG_frame.grid(row=15, padx=(80, 0), columnspan=2, sticky='w')
	boss_DMG = BinaryStats(boss_DMG_frame, 50, 0, 'Boss DMG %')

	# DMG bonus
	bonus_DMG_frame = ttk.Frame(root, style = 'dark_frame')
	bonus_DMG_frame.grid(row=16, padx=(80, 0), columnspan=2, sticky='w')
	bonus_DMG = BinaryStats(bonus_DMG_frame, 100, 0, 'DMG bonus %')


	# ele DMG %
	e_DMG_per_frame = ttk.Frame(root, style = 'dark_frame')
	e_DMG_per_frame.grid(row=17, pady=(0, 10), padx=(80, 0), columnspan=2, sticky='w')
	e_DMG = BinaryStats(e_DMG_per_frame, 100, 0, 'Ele DMG %')




	root.mainloop()

class Atk:
	def __init__(self, root, stat_increase: int) -> None:
		self.stat_increase = stat_increase
		self.root = root
		self.stats_row = 0

		# row 1
		# base atk
		self.base_atk = LabelEntry(self.root, 0, 0, 'base ATK', 1000, lambda e: self.set_progress(), padx= (0, 120))

		# increase
		self.increase = LabelEntry(self.root, 0, 2, '+ ATK', self.stat_increase, lambda e: self.set_progress())

		#progress_mod
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row , column=4, padx= (200,20))

		# row 2
		# bonus atk %
		self.bonus_atk_percent = LabelEntry(self.root, 1, 0, 'ATK bonus %', 0, lambda e : self.set_progress(), padx= (0, 120),
											tooltip='% atk from gear, card, etc.')

		# bonus atk
		self.bonus_atk = LabelEntry(self.root, 1, 2, 'ATK bonus', 0, lambda e : self.set_progress(),
									tooltip='flat atk from other source (skill, pet, etc.)')

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		base = self.base_atk.get()
		bonus = self.bonus_atk.get()
		bonus_perc = self.bonus_atk_percent.get() / 100
		# calculate increase
		DPS_multiplier = (1 + (base + increase * (1 + bonus_perc / 100) + bonus) / 700)
		return DPS_multiplier

	def calc_increase(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(self.increase.get())
		increase = (stat_increase - stat) / (stat - 1) * 100
		return increase

	def set_progress(self) -> None:
		increase = self.calc_increase()
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label3 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label3.grid(row=self.stats_row, column=5)

	def get(self) -> float:
		return self.calc_DPS_increase()

class ElementAtk:
	def __init__(self, root, stat_increase: int) -> None:
		self.stat_increase = stat_increase
		self.root = root
		self.stats_row = 0

		# row 1
		# base e.atk
		self.base_atk = LabelEntry(self.root, 0, 0, 'E-ATK', 250, lambda e : self.set_progress(), padx=(0, 120))

		# increase
		self.increase = LabelEntry(self.root, 0, 2, '+ E-ATK', 17, lambda e : self.set_progress())

		# progress_mod bar
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row, column=4, padx= (200,20))

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		base = self.base_atk.get()

		# calculate increase
		DPS_multiplier = (1 + (base + increase) / 700)
		return DPS_multiplier

	def calc_increase(self)  -> float:

		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(self.increase.get())
		increase = (stat_increase - stat) / (stat - 1) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label3 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label3.grid(row=self.stats_row, column=5)

	def get(self):
		return self.calc_DPS_increase()

class Crit:
	def __init__(self, root, stat_increase_mod: int, stat_increase_DMG: int) -> None:
		self.root = root
		self.stats_row = 0

		# row 1
		# crit mod
		self.crit_mod = LabelEntry(self.root, 0, 0, 'CRIT mod', 100, lambda e : self.set_progress(), padx=(0, 120))

		# increase crit mod
		self.increase_mod = LabelEntry(self.root, 0, 2, '+ CRIT mod', stat_increase_mod, lambda e : self.set_progress_mod())

		#progress_mod bar
		self.progress_mod = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress_mod.grid(row=self.stats_row, column=4, padx= (200, 20))

		# row 2
		# bonus CRIT rate
		self.bonus_crit_rate = LabelEntry(self.root, 1, 0, 'bonus CRIT rate', 0, lambda e : self.set_progress(), padx=(0, 120))

		# CRIT resist
		self.crit_resist = LabelEntry(self.root, 1, 2, 'CRIT resist %', 0, lambda e : self.set_progress(),
									  tooltip= 'enemy CRIT rate resistance')

		#row 3
		# CRIT DMG
		self.crit_dmg = LabelEntry(self.root, 2, 0, 'CRIT DMG', 150, lambda e : self.set_progress(), padx=(0, 120))

		# increase crit DMG
		self.increase_DMG = LabelEntry(self.root, 2, 2, '+ CRIT DMG', stat_increase_DMG, lambda e : self.set_progress_DMG())

		#progess bar
		self.progress_DMG = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress_DMG.grid(row=self.stats_row + 2, column=4, padx=(200, 20))

		#row 4
		# bonus CRIT DMG
		self.b_crit_dmg = LabelEntry(self.root, 3, 0, 'bonus CRIT DMG', 0, lambda e : self.set_progress(), padx=(0, 120))

	def calc_DPS_increase(self, increase_mod: float = 0, increase_DMG: float = 0) -> float:
		# get value
		crit_mod = self.crit_mod.get()
		crit_dmg = self.crit_dmg.get()
		crit_mod += increase_mod
		crit_dmg += increase_DMG

		# calculate crit rate
		crit_rate = self.calc_crit_rate(crit_mod)

		print(f"crit_rate: {crit_rate}, crit dmg: {crit_dmg}")

		if crit_rate >= 1:
			DPS_multiplier = crit_dmg
		else:
			DPS_multiplier = 1 + (crit_dmg * crit_rate / 100)

		print(f"DPS_multiplier: {DPS_multiplier}")
		print(f"")


		return DPS_multiplier

	def calc_increase_mod(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(increase_mod= self.increase_mod.get())
		print(f"stat_increase: {stat_increase}, stat: {stat}")
		increase = ((stat_increase - stat) / stat) * 100
		return increase

	def calc_increase_DMG(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(increase_DMG= self.increase_DMG.get())
		print(f"stat_increase: {stat_increase}, stat: {stat}")
		increase = ((stat_increase - stat) / stat) * 100
		return increase

	def set_progress_mod(self):
		increase = self.calc_increase_mod()
		crit_rate = self.calc_crit_rate(self.crit_mod.get())
		self.progress_mod.config(maximum=10)
		self.progress_mod.config(value=increase)

		label3 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label3.grid(row=self.stats_row, column=5)

		label5 = tk.Label(self.root, text=f"{crit_rate * 100:.2f}% CRIT rate", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label5.grid(row=self.stats_row + 1, column=4, padx=(200, 20))

	def set_progress_DMG(self):
		increase = self.calc_increase_DMG()
		self.progress_DMG.config(maximum=10)
		self.progress_DMG.config(value=increase)

		label4 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label4.grid(row=self.stats_row + 2, column=5)

	def set_progress(self):
		self.set_progress_mod()
		self.set_progress_DMG()

	def get(self):
		return self.calc_DPS_increase()

	def calc_crit_rate(self, crit_mod: float) -> float:
		b_crit_rate = self.bonus_crit_rate.get() / 100

		# calculate increase
		if crit_mod <= 200 :
			crit_rate = crit_mod / 400
		if 200 < crit_mod <= 500 :
			crit_rate = crit_mod * 17 / 6000 - crit_mod ** 2 / 600000
		if 500 < crit_mod :
			crit_rate = crit_mod / 500
		crit_rate = crit_rate - self.crit_resist.get() / 100 + b_crit_rate
		crit_rate = crit_rate if crit_rate <= 1 else 1
		return crit_rate

class BinaryStats:
	def __init__(self, root, initial_stat: int, stat_increase: int, stat_name: str) -> None:
		self.root = root
		self.stats_row = 0

		# row 1
		# base stat
		self.stat = LabelEntry(self.root, 0, 0, stat_name, initial_stat, lambda e : self.set_progress(), padx=(0, 120))

		# increase
		self.increase = LabelEntry(self.root, 0, 2, f"+ {stat_name}", stat_increase, lambda e : self.set_progress())

		# progress_mod bar
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row, column=4, padx= (200,20))

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		base = self.stat.get() / 100
		# calculate increase
		DPS_multiplier = 1 + (base + increase / 100)
		return DPS_multiplier

	def calc_increase(self)  -> float:

		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(self.increase.get())
		increase = (stat_increase - stat) / (stat - 1) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label3 = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label3.grid(row=self.stats_row, column=5)

	def get(self):
		return self.calc_DPS_increase()

class DefIgn:
	def __init__(self, root, stat_increase: int) -> None:
		self.root = root
		self.stats_row = 0

		# row 1
		# Def Ignore
		self.def_ignore = LabelEntry(self.root, 0, 0, 'DEF Ignore', 5000, lambda e : self.set_progress(), padx=(0, 120))

		# increase
		self.increase = LabelEntry(self.root, 0, 2, '+ DEF Ignore', stat_increase, lambda e : self.set_progress())

		#progress
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row , column=4, padx= (200,20))

		# row 2
		# enemy Def
		self.defense = LabelEntry(self.root, 1, 0, 'enemy DEF', 6800, lambda e : self.set_progress(), padx= (0, 120))

		# Def shred
		self.def_shred = LabelEntry(self.root, 1, 2, 'DEF shred', 0, lambda e : self.set_progress(),
									tooltip= 'def shred (soul ord, skill, etc.')

		# row 3
		# Def shred %
		self.def_shred_per = LabelEntry(self.root, 2, 0, 'DEF shred %', 0, lambda e : self.set_progress(), padx=(0, 120),
										tooltip= '% def shred (ninja talent)')

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		di = self.def_ignore.get() + increase
		defense = self.calc_def()
		delta = defense - di

		if delta <= 0:
			DPS_multiplier = 1
		else:
			DPS_multiplier = 1505 / (1505 + delta)

		return DPS_multiplier

	def calc_increase(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(self.increase.get())
		increase = (stat_increase - stat) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		damage_lost = (1 - self.calc_DPS_increase()) * 100
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label.grid(row=self.stats_row, column=5)

		label2 = tk.Label(self.root, text=f"losing {damage_lost:.2f}% DPS to DI", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label2.grid(row=self.stats_row + 1, column=4, padx=(200, 20))

	def calc_def(self) -> float:
		# get value
		base = self.defense.get()
		per_shred = self.def_shred_per.get() / 100
		flat_shred = self.def_shred.get()

		defense = base * (1 - per_shred) - flat_shred
		return defense

	def get(self):
		return self.calc_DPS_increase()

class Ep:
	def __init__(self, root, stat_increase: int) -> None:
		self.root = root
		self.stats_row = 0

		# row 1
		# Def Ignore
		self.ep = LabelEntry(self.root, 0, 0, 'ep', 1500, lambda e : self.set_progress(), padx=(0, 120))

		# increase
		self.increase = LabelEntry(self.root, 0, 2, '+ EP', stat_increase, lambda e : self.set_progress())

		#progress
		self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
		self.progress.grid(row=self.stats_row , column=4, padx= (200,20))

		# row 2
		# enemy Def
		self.e_def = LabelEntry(self.root, 1, 0, 'enemy E-DEF', 2600, lambda e : self.set_progress(), padx=(0, 120))

		# Def shred
		self.e_def_shred = LabelEntry(self.root, 1, 2, 'EP shred', 0, lambda e : self.set_progress())

	def calc_DPS_increase(self, increase: float = 0) -> float:
		# get value
		ep = self.ep.get() + increase
		e_defense = self.calc_def()

		if ep > e_defense:
			DPS_multiplier = 1 + ((ep - e_defense) / ( ep- e_defense + 3992))
		else:
			DPS_multiplier = 1505 / (1505 + e_defense - ep)

		return DPS_multiplier

	def calc_increase(self)  -> float:
		stat = self.calc_DPS_increase()
		stat_increase = self.calc_DPS_increase(self.increase.get())
		increase = (stat_increase - stat) * 100
		return increase

	def set_progress(self):
		increase = self.calc_increase()
		damage_lost = (1 - self.calc_DPS_increase()) * 100
		self.progress.config(maximum=10)
		self.progress.config(value=increase)
		label = tk.Label(self.root, text=f" +{increase:.2f}% DPS", anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label.grid(row=self.stats_row, column=5)

		if damage_lost > 0:
			text = f"losing {damage_lost:.2f}% DPS to EP"
		else:
			text = "no losing DPS to EP"
		label2 = tk.Label(self.root, text=text, anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		label2.grid(row=self.stats_row + 1, column=4, padx=(200, 20))

	def calc_def(self) -> float:
		# get value
		base = self.e_def.get()
		flat_shred = self.e_def_shred.get()

		e_defense = base - flat_shred
		return e_defense

	def get(self):
		return self.calc_DPS_increase()

class LabelEntry:
	def __init__(self, root: tk.Frame,
				 row: int,
				 column: int,
				 text: str,
				 startingvalue: int,
				 func,
				 tooltip: str = '',
				 padx: tuple[float, float] = (0, 0)
				 ) -> None:
		self.root = root
		self.tooltip_text = tooltip
		self.tooltip = None

		self.label = tk.Label(self.root, text=text, anchor='w', width=20, background= '#2b2b2b', foreground= '#a2aaa4')
		self.label.grid(row=row, column= column)

		self.entry = tk.Entry(self.root, background= '#323232', foreground= '#a2aaa4', insertbackground="#a2aaa4")
		self.entry.insert(startingvalue, str(startingvalue))
		self.entry.grid(row=row, column= column + 1, sticky='w', padx= padx)

		self.entry.bind("<Return>", lambda event : func(event))
		if self.tooltip_text:
			self.label.bind("<Enter>", self.show_tooltip)
			self.label.bind("<Leave>", self.hide_tooltip)

	def show_tooltip(self, event) :
		x = event.x_root
		y = event.y_root

		self.tooltip = tk.Toplevel()
		self.tooltip.geometry(f"+{x}+{y + 20}")
		self.tooltip.overrideredirect(True)

		label = tk.Label(self.tooltip, text=self.tooltip_text, background= '#a2aaa4', foreground= '#2b2b2b')
		label.pack(ipadx=1, ipady=1)

	def hide_tooltip(self, event) :
		if self.tooltip :
			self.tooltip.destroy()
			self.tooltip = None

	def get(self):
		value = float(self.entry.get())
		return value

if __name__ == '__main__':
	main()
