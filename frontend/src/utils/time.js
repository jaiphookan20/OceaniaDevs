export const getRelativeTimeString = (date) => {
    const now = new Date();
    const applicationDate = new Date(date);
    const diffTime = Math.abs(now - applicationDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return '1 day ago';
    } else if (diffDays <= 7) {
      return 'This week';
    } else if (diffDays <= 14) {
      return '1w ago';
    } else if (diffDays <= 30) {
      return `${Math.floor(diffDays / 7)}w ago`;
    } else if (diffDays <= 60) {
      return '1mo ago';
    } else {
      return `${Math.floor(diffDays / 30)}m ago`;
    }
  };