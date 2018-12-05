import Tkinter
import project3

DEFAULT_FONT = ('Helvetica', 10)

class SearchWindow:
	def __init__(self):
		self.root_window = Tkinter.Tk()
		self.root_window.wm_title('Search Engine')
		search_title = Tkinter.Label(
			master = self.root_window, text = "UCI ICS Web Search",
			font = DEFAULT_FONT)
		search_title.grid(row = 0, column = 0, padx = 10, pady = 10)
		self.entry_box = Tkinter.Entry(
			master = self.root_window)
		self.entry_box.grid(row = 1, column = 0, padx = 10, pady = 10)
		search_button = Tkinter.Button(
			master = self.root_window, text = "Search", font = DEFAULT_FONT,
			command = self.on_search_button)
		search_button.grid(
			row = 1, column = 1, padx = 10, pady = 10,
			sticky = Tkinter.W)
	def run(self):
		self.root_window.mainloop()
	def on_search_button(self):
		search_query = self.entry_box.get()
		self.entry_box.delete(0,'end')
		result_urls = project3.search(search_query)
		result_window = ResultWindow(result_urls)
		result_window.show()

class ResultWindow:
	def __init__(self, result_urls):
		self.result_urls = result_urls
		self.result_window = Tkinter.Toplevel()
		self.result_window.wm_title("Search Result")
		# scroll = Tkinter.Scrollbar(master = self.result_window)
		# scroll.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
		self.result_box = Tkinter.Text(
			master = self.result_window, font = DEFAULT_FONT)
		self.result_box.grid(row = 0, column = 0, padx = 20, pady = 20)
		# scroll.config(command=self.result_box.yview)
		self.show_results()
	def show(self):
		self.result_window.grab_set()
		self.result_window.wait_window()
	def show_results(self):
		for i in range(len(self.result_urls)):
			self.result_box.insert(Tkinter.END,self.result_urls[i] + '\n\n')

if __name__ == '__main__':
	new_window = SearchWindow()
	new_window.run()
